// Ported from AutoLab source commit 1255884; see docs/SOURCE_MANIFEST.json.

import React, { createContext, Suspense, useCallback, useContext, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { addAfterEffect, Canvas, useThree } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import { Group, Light, Mesh, MeshStandardMaterial, PMREMGenerator, PerspectiveCamera, type Texture } from "three";
import { applyCabinTrim, createTrimMaps } from "@/src/lib/three/cabin-trim";
import { DEFAULT_TRIM_ID } from "@/src/lib/trim-specification";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { createKtx2Runtime } from "@/src/lib/three/ktx2-runtime";
import { attachThreadMask } from "@/src/lib/three/thread-mask";
import type { Treatment as UpholsteryTreatment, RuntimeCamera as CameraViewId } from "./configuration-adapter";

import { LEXUS_CAMERA_PRESETS } from "@/src/config/lexus-camera-presets";
import { LEXUS_L4_ASSET_URLS } from "@/src/config/lexus-runtime-assets";

const ALL_CAMERA_PRESETS: Record<string, {
  target: readonly [number, number, number];
  position: readonly [number, number, number];
  fov?: number;
}> = {
  ...LEXUS_CAMERA_PRESETS,
};

// Sources: https://r3f.docs.pmnd.rs/api/canvas,
// https://drei.docs.pmnd.rs/loaders/gltf-use-gltf,
// https://threejs.org/docs/pages/RoomEnvironment.html,
// https://threejs.org/docs/pages/GLTFLoader.html.
const LEXUS_L4_DIAMOND_ASSET_URL = LEXUS_L4_ASSET_URLS.diamond;
// Active Lexus RX 350 L2B interior assembly contract (all 7 slots)
const LEXUS_SEAT_PRIMARY = "MAT_Seat_Primary";
const LEXUS_SEAT_SECONDARY = "MAT_Seat_Secondary";
const LEXUS_SEAT_STITCHING = "MAT_Seat_Stitching";
const LEXUS_STEERING_LEATHER = "MAT_Steering_Leather";
const LEXUS_DASHBOARD_TRIM = "MAT_Dashboard_Trim";
const LEXUS_COCKPIT_ACCENT = "MAT_Cockpit_Accent";
const LEXUS_COCKPIT_BLACK = "MAT_Cockpit_Black";

// Legacy Mercedes-Benz S-Class spike contract (preserved for historical regression)
const LEGACY_SEAT_SLOT = "MAT_Upholstery_Primary";
const LEGACY_OLED_SLOT = "MAT_Screen_Central_OLED";

type ViewerStatus = "loading" | "success" | "empty" | "error";
export type RendererStats = { calls: number; triangles: number; textures: number; geometries: number };
type MaterialState = {
  bindings: Record<string, string>; colors: Record<string, string>;
  textures?: Record<string, { uuid: string; compressed: boolean; mips: number } | null>;
  quiltThread?: boolean;
  trim?: { id: string; map: string | null; compressed: boolean; surfaces: string[]; roughness: number; environment: number };
  ambient?: string[];
};
export type ViewerEvidence = {
  status: ViewerStatus;
  assetUrl: string;
  materialState: MaterialState | null;
  renderer: RendererStats | null;
  error: string | null;
  cameraFov?: number;
  cameraPosition?: number[];
  treatment?: UpholsteryTreatment;
};

declare global {
  interface Window {
    __autolab?: { snapshot: () => ViewerEvidence; loseContext: () => boolean };
  }
}

function testParam(key: string) {
  return import.meta.env.VITE_E2E === "1" && typeof window !== "undefined" && new URLSearchParams(window.location.search).has(key);
}

function getAssetUrl(treatment: UpholsteryTreatment = "classic") {
  if (testParam("missing-asset")) return `${import.meta.env.BASE_URL}assets/3d/missing.glb`;
  return LEXUS_L4_ASSET_URLS[treatment];
}

const StudioEnvironment = createContext<Texture | null>(null);
function RoomLighting({ ambientHex, children }: { ambientHex: string; children: React.ReactNode }) {
  const { gl, invalidate } = useThree();
  const [environment, setEnvironment] = useState<Texture | null>(null);
  useEffect(() => {
    const room = new RoomEnvironment();
    const generator = new PMREMGenerator(gl);
    const target = generator.fromScene(room);
    const frame = window.requestAnimationFrame(() => { setEnvironment(target.texture); invalidate(); });
    return () => {
      window.cancelAnimationFrame(frame);
      target.dispose();
      generator.dispose();
      room.dispose();
    };
  }, [gl, invalidate]);
  return <>{environment && <primitive attach="environment" object={environment} />}<ambientLight intensity={0.35} /><directionalLight position={[3, 2, 0]} intensity={1.2} />
    {/* Concealed wash beneath the dashboard and over the console; no shadow maps or extra geometry. */}
    <pointLight name="AutoLabAmbientLeft" position={[-.42,.72,.38]} color={ambientHex} intensity={.18} distance={.85} decay={2}/>
    <pointLight name="AutoLabAmbientRight" position={[.42,.72,.38]} color={ambientHex} intensity={.18} distance={.85} decay={2}/>
    <pointLight name="AutoLabAmbientConsole" position={[0,.78,.05]} color={ambientHex} intensity={.06} distance={.65} decay={2}/>
    <StudioEnvironment.Provider value={environment}>{children}</StudioEnvironment.Provider>
  </>;
}

function syncCameraRig(
  cam: unknown,
  ctrls: React.ElementRef<typeof OrbitControls> | null,
  preset: { position: readonly [number, number, number]; target: readonly [number, number, number]; fov?: number },
) {
  if (cam instanceof PerspectiveCamera) {
    cam.position.set(preset.position[0], preset.position[1], preset.position[2]);
    const targetFov = preset.fov ?? 38;
    if (cam.fov !== targetFov) {
      cam.fov = targetFov;
    }
    cam.updateProjectionMatrix();
  }
  ctrls?.target.set(preset.target[0], preset.target[1], preset.target[2]);
  ctrls?.update();
}

function CameraRig({ view }: { view: CameraViewId }) {
  const { camera, invalidate } = useThree();
  const controls = useRef<React.ElementRef<typeof OrbitControls>>(null);
  const [reducedMotion, setReducedMotion] = useState(false);
  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReducedMotion(media.matches);
    update();
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);
  useEffect(() => {
    // Fixed evidence viewpoints exist only in explicitly enabled local E2E builds.
    // They do not change the four customer presets, orbit limits or render context.
    const preset = testParam("review-carbon-dashboard")
      ? { position: [-.38, .97, .16] as const, target: [-.47, .855, .55] as const, fov: 40 }
      : testParam("review-carbon-console")
        ? { position: [.16, 1.03, -.05] as const, target: [0, .58, .17] as const, fov: 40 }
        : ALL_CAMERA_PRESETS[view] ?? LEXUS_CAMERA_PRESETS.hero_driver;
    syncCameraRig(camera, controls.current, preset);
    invalidate();
  }, [camera, invalidate, view]);
  return <OrbitControls ref={controls} makeDefault enablePan={false} enableDamping={!reducedMotion}
    minDistance={0.35} maxDistance={4} minPolarAngle={0.15} maxPolarAngle={Math.PI * 0.82} />;
}

interface ExtractedModel {
  isLexus: boolean;
  isCompleteAssembly: boolean;
  materials: Record<string, MeshStandardMaterial>;
  bindings: Record<string, string>;
}

function materialEvidence(parsed: ExtractedModel): MaterialState {
  const colors = Object.fromEntries(Object.entries(parsed.materials).map(([name, mat]) => [name, "#" + mat.color.getHexString()]));
  const result: MaterialState = { bindings: parsed.bindings, colors };
  if (import.meta.env.VITE_E2E === "1") {
    result.textures = {};
    for (const name of [LEXUS_SEAT_PRIMARY, LEXUS_SEAT_SECONDARY]) {
      for (const role of ["map", "normalMap", "roughnessMap"] as const) {
        const texture = parsed.materials[name]?.[role];
        result.textures[name + ":" + role] = texture ? {
          uuid: texture.uuid, compressed: "isCompressedTexture" in texture && texture.isCompressedTexture === true,
          mips: texture.mipmaps.length,
        } : null;
      }
    }
    result.quiltThread = parsed.materials[LEXUS_SEAT_PRIMARY]?.customProgramCacheKey().includes("autolab-l4a-thread-v1") ?? false;
    const trim = parsed.materials.MAT_Console_Carbon;
    if (trim) result.trim = {
      id: trim.userData.trimPreview, map: trim.map?.uuid ?? null,
      compressed: Boolean(trim.map && 'isCompressedTexture' in trim.map && trim.map.isCompressedTexture),
      surfaces: Object.entries(parsed.bindings).filter(([,name]) => name === 'MAT_Console_Carbon').map(([name]) => name),
      roughness: trim.roughness, environment: trim.envMapIntensity,
    };
  }
  return result;
}

function modelMaterials(scene: Group): ExtractedModel | null {
  const materials: Record<string, MeshStandardMaterial> = {};
  const bindings: Record<string, string> = {};

  scene.traverse((object) => {
    if (object instanceof Mesh) {
      const mats = Array.isArray(object.material) ? object.material : [object.material];
      for (const m of mats) {
        if (m instanceof MeshStandardMaterial && m.name) {
          materials[m.name] = m;
          bindings[object.name] = m.name;
        }
      }
    }
  });

  const materialNames = Object.keys(materials);
  if (materialNames.length === 0) return null;

  // Active Lexus RX 350 Assembly (7-slot L2B interior or 3-slot L2A driver-seat rollback)
  if (materials[LEXUS_SEAT_PRIMARY]) {
    if (!materials[LEXUS_SEAT_SECONDARY] || !materials[LEXUS_SEAT_STITCHING]) {
      throw new Error("Lexus asset is missing required secondary or stitching material slot");
    }
    // GLTFLoader can swallow texture decode errors and return untextured materials.
    for (const name of [LEXUS_SEAT_PRIMARY, LEXUS_SEAT_SECONDARY]) {
      for (const role of ["map", "normalMap", "roughnessMap"] as const) {
        if (!materials[name][role]) throw new Error(`Required Lexus texture failed to decode: ${name}.${role}`);
      }
    }
    const isComplete = Boolean(
      materials[LEXUS_STEERING_LEATHER] &&
      materials[LEXUS_DASHBOARD_TRIM] &&
      materials[LEXUS_COCKPIT_ACCENT] &&
      materials[LEXUS_COCKPIT_BLACK]
    );
    return { isLexus: true, isCompleteAssembly: isComplete, materials, bindings };
  }

  // Legacy Mercedes Spike compatibility (preserved for historical regression)
  if (materials[LEGACY_SEAT_SLOT]) {
    if (!materials[LEGACY_OLED_SLOT]) {
      throw new Error("Legacy Mercedes spike missing OLED material contract");
    }
    return { isLexus: false, isCompleteAssembly: false, materials, bindings };
  }

  throw new Error("Unrecognized 3D asset material contract: " + materialNames.join(", "));
}

function SpikeModel({
  url,
  ktxRuntime,
  trimMaps,
  trimId = DEFAULT_TRIM_ID,
  ambientHex = '#38B6FF',
  treatment = "classic",
  primaryHex,
  secondaryHex = primaryHex,
  threadHex = "#D4AF37",
  trimHex = "#2A2B2E",
  steeringHex = secondaryHex,
  accentHex = "#787D82",
  cockpitBlackHex = "#121316",
  onLoaded,
  onStats,
}: {
  url: string;
  ktxRuntime: ReturnType<typeof createKtx2Runtime>;
  trimMaps: ReturnType<typeof createTrimMaps>;
  trimId?: string;
  ambientHex?: string;
  treatment?: UpholsteryTreatment;
  primaryHex: string;
  secondaryHex?: string;
  threadHex?: string;
  trimHex?: string;
  steeringHex?: string;
  accentHex?: string;
  cockpitBlackHex?: string;
  onLoaded: (state: MaterialState | null, url: string) => void;
  onStats: (stats: RendererStats, url: string) => void;
}) {
  const { gl, invalidate, scene: renderScene } = useThree();
  const environment = useContext(StudioEnvironment);

  // Local Draco and KTX2 loader configuration
  const { scene } = useGLTF(url, `${import.meta.env.BASE_URL}draco/`, false, (loader) => {
    ktxRuntime.trackURL(url);
    loader.setKTX2Loader(ktxRuntime.loader);
  }) as { scene: Group };

  const parsed = useMemo(() => modelMaterials(scene), [scene]);
  const previewMaps = parsed?.materials.MAT_Console_Carbon ? trimMaps.read() : null;

  // Install before the first rendered frame, including a cached Suspense reveal.
  // A passive effect can run after the readiness sample and leave stale evidence.
  useLayoutEffect(() => {
    if (!parsed || !parsed.isLexus) return;
    const { materials } = parsed;
    if (treatment === "diamond" && url === LEXUS_L4_DIAMOND_ASSET_URL && materials[LEXUS_SEAT_PRIMARY] && materials[LEXUS_SEAT_STITCHING]) {
      const cleanup = attachThreadMask(materials[LEXUS_SEAT_PRIMARY], materials[LEXUS_SEAT_STITCHING]);
      return cleanup;
    }
  }, [parsed, treatment, url]);

  useEffect(() => {
    if (!parsed) {
      onLoaded(null, url);
      return;
    }
    // Success is reported only after this model has rendered below.
  }, [parsed, onLoaded, url]);

  // React reconnects layout effects when Suspense reveals a cached scene again.
  // A passive effect with unchanged Classic props would not acknowledge that frame.
  // https://react.dev/reference/react/Suspense#caveats
  useLayoutEffect(() => {
    if (!parsed) return;
    const { materials, isLexus } = parsed;

    if (isLexus) {
      if (previewMaps && materials.MAT_Console_Carbon) applyCabinTrim(materials.MAT_Console_Carbon, trimId, previewMaps, environment);
      if (!testParam("break-seat-binding") && materials[LEXUS_SEAT_PRIMARY]) {
        materials[LEXUS_SEAT_PRIMARY].color.set(primaryHex);
      }
      if (materials[LEXUS_SEAT_SECONDARY]) {
        materials[LEXUS_SEAT_SECONDARY].color.set(secondaryHex);
      }
      if (materials[LEXUS_SEAT_STITCHING]) {
        materials[LEXUS_SEAT_STITCHING].color.set(threadHex);
      }
      if (materials[LEXUS_STEERING_LEATHER]) {
        materials[LEXUS_STEERING_LEATHER].color.set(steeringHex ?? secondaryHex);
      }
      if (materials[LEXUS_DASHBOARD_TRIM]) {
        materials[LEXUS_DASHBOARD_TRIM].color.set(trimHex ?? "#2A2B2E");
      }
      if (materials[LEXUS_COCKPIT_ACCENT]) {
        materials[LEXUS_COCKPIT_ACCENT].color.set(accentHex ?? "#787D82");
      }
      if (materials[LEXUS_COCKPIT_BLACK]) {
        materials[LEXUS_COCKPIT_BLACK].color.set(cockpitBlackHex ?? "#121316");
      }
    } else {
      if (!testParam("break-seat-binding") && materials[LEGACY_SEAT_SLOT]) {
        materials[LEGACY_SEAT_SLOT].color.set(primaryHex);
      }
    }

    // Sample after a rendered frame, not a timer that can beat shader compilation.
    let pending = true;
    const unsubscribe = addAfterEffect(() => {
      if (!pending || gl.info.render.calls === 0) return;
      pending = false;
      const evidence = materialEvidence(parsed);
      if (import.meta.env.VITE_E2E === '1') {
        evidence.ambient = [];
        renderScene.traverse(object => {
          if (object instanceof Light && object.name.startsWith('AutoLabAmbient')) evidence.ambient!.push('#'+object.color.getHexString());
        });
      }
      onLoaded(evidence, url);
      onStats({
        calls: gl.info.render.calls,
        triangles: gl.info.render.triangles,
        textures: gl.info.memory.textures,
        geometries: gl.info.memory.geometries,
      }, url);
    });
    invalidate();
    return unsubscribe;
  }, [parsed, previewMaps, environment, trimId, ambientHex, renderScene, primaryHex, secondaryHex, threadHex, trimHex, steeringHex, accentHex, cockpitBlackHex, invalidate, onLoaded, onStats, gl, url]);

  return <primitive object={scene} />;
}

// Own decoder workers outside Suspense, so suspended/failed models still get cleanup.
function ModelLoaderScope({ onLoading, ...props }: Omit<React.ComponentProps<typeof SpikeModel>, "ktxRuntime" | "trimMaps"> & { onLoading: () => void }) {
  const { gl } = useThree();
  const [runtime] = useState(() => createKtx2Runtime(gl, (url) => useGLTF.clear(url)));
  const [trimMaps] = useState(() => createTrimMaps(url => runtime.loader.loadAsync(url)));
  useEffect(() => { runtime.acquire(); trimMaps.acquire(); return () => { trimMaps.release(); runtime.release(); }; }, [runtime, trimMaps]);
  useLayoutEffect(() => { onLoading(); }, [props.url, onLoading]);
  return <Suspense fallback={null}><SpikeModel {...props} ktxRuntime={runtime} trimMaps={trimMaps} /></Suspense>;
}

class SceneBoundary extends React.Component<{ children: React.ReactNode; onError: (message: string) => void }, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  componentDidCatch(error: Error) { this.props.onError(error.message); }
  render() { return this.state.failed ? null : this.props.children; }
}

export function RuntimeViewer({
  view,
  trimId = DEFAULT_TRIM_ID,
  ambientHex = '#38B6FF',
  treatment = "classic",
  primaryHex,
  secondaryHex = primaryHex,
  threadHex = "#D4AF37",
  trimHex = "#2A2B2E",
  steeringHex = secondaryHex,
  accentHex = "#787D82",
  cockpitBlackHex = "#121316",
  onStatus,
  onStats,
}: {
  view: CameraViewId;
  trimId?: string;
  ambientHex?: string;
  treatment?: UpholsteryTreatment;
  primaryHex: string;
  secondaryHex?: string;
  threadHex?: string;
  trimHex?: string;
  steeringHex?: string;
  accentHex?: string;
  cockpitBlackHex?: string;
  onStatus: (status: ViewerStatus) => void;
  onStats: (stats: RendererStats | null) => void;
}) {
  const [supported, setSupported] = useState(false);
  const [status, setStatus] = useState<ViewerStatus>("loading");
  const [error, setError] = useState<string | null>(null);
  const [materialState, setMaterialState] = useState<MaterialState | null>(null);
  const [renderer, setRenderer] = useState<RendererStats | null>(null);
  const [retryKey, setRetryKey] = useState(0);
  const cameraRef = useRef<PerspectiveCamera | null>(null);
  const contextRef = useRef<WebGLRenderingContext | WebGL2RenderingContext | null>(null);
  const cleanupRef = useRef<(() => void) | null>(null);
  const url = getAssetUrl(treatment);
  const requestedUrl = useRef(url);
  useLayoutEffect(() => { requestedUrl.current = url; }, [url]);
  const fail = useCallback((message: string) => {
    // Canvas disposal intentionally loses its context. Preserve the original
    // loader error instead of treating teardown as a second runtime failure.
    cleanupRef.current?.();
    cleanupRef.current = null;
    setError(message);
    setStatus("error");
    onStatus("error");
    onStats(null);
  }, [onStatus, onStats]);
  const loaded = useCallback((state: MaterialState | null, loadedUrl: string) => {
    if (loadedUrl !== requestedUrl.current) return;
    if (!state) { setStatus("empty"); onStatus("empty"); return; }
    setMaterialState(state);
    setStatus("success");
    onStatus("success");
  }, [onStatus]);
  const stats = useCallback((value: RendererStats, loadedUrl: string) => {
    if (loadedUrl !== requestedUrl.current) return;
    setRenderer(value); onStats(value);
  }, [onStats]);
  const loading = useCallback(() => {
    setError(null); setMaterialState(null); setRenderer(null);
    setStatus("loading"); onStatus("loading"); onStats(null);
  }, [onStatus, onStats]);

  useEffect(() => {
    if (status !== 'loading') return;
    const timer = window.setTimeout(() => fail('Loading took too long. Check the local server and retry.'), 45_000);
    return () => window.clearTimeout(timer);
  }, [status, url, retryKey, fail]);

  useEffect(() => {
    const probeTimer = window.setTimeout(() => {
      const probe = document.createElement("canvas");
      const context = probe.getContext("webgl2");
      if (!context) { fail("WebGL2 is unavailable"); return; }
      context.getExtension("WEBGL_lose_context")?.loseContext();
      setSupported(true);
    }, 0);
    return () => { window.clearTimeout(probeTimer); cleanupRef.current?.(); };
  }, [fail]);

  useEffect(() => {
    if (import.meta.env.VITE_E2E !== "1") return;
    const currentFov = (ALL_CAMERA_PRESETS[view] ?? LEXUS_CAMERA_PRESETS.hero_driver).fov ?? 38;
    window.__autolab = {
      snapshot: () => ({ status, assetUrl: url, materialState, renderer, error, cameraFov: cameraRef.current?.fov ?? currentFov, cameraPosition: cameraRef.current?.position.toArray(), treatment }),
      loseContext: () => {
        const extension = contextRef.current?.getExtension("WEBGL_lose_context");
        if (!extension) return false;
        extension.loseContext();
        return true;
      },
    };
    return () => { delete window.__autolab; };
  }, [status, url, materialState, renderer, error, view, treatment]);

  const retry = () => {
    useGLTF.clear(url);
    cleanupRef.current?.();
    cleanupRef.current = null;
    setError(null); setMaterialState(null); setRenderer(null);
    setStatus("loading"); onStatus("loading"); onStats(null);
    setRetryKey((value) => value + 1);
  };

  // Suspense may hide a previous scene during a GLB switch. Use a neutral stage,
  // never the historical illustration. https://react.dev/reference/react/Suspense
  return <div className="absolute inset-0 z-10" style={{ backgroundColor: status === 'error' || status === 'empty' ? 'transparent' : '#0F1014' }}
    data-testid="spike-viewer" aria-busy={status === 'loading'} aria-label="AutoLab interactive 3D interior viewer">
    {supported && status !== "error" && status !== "empty" && <Canvas key={retryKey} frameloop="demand" dpr={[1, 1.5]}
      camera={{
        fov: (ALL_CAMERA_PRESETS[view] ?? LEXUS_CAMERA_PRESETS.hero_driver).fov ?? 38,
        near: 0.05,
        far: 10,
        position: (ALL_CAMERA_PRESETS[view] ?? LEXUS_CAMERA_PRESETS.hero_driver).position,
      }}
      gl={{ antialias: true, powerPreference: "high-performance" }}
      onCreated={({ gl, camera }) => {
        cameraRef.current = camera as PerspectiveCamera;
        contextRef.current = gl.getContext();
        const canvas = gl.domElement;
        const lost = (event: Event) => { event.preventDefault(); fail("WebGL context lost"); };
        const restored = () => retry();
        canvas.addEventListener("webglcontextlost", lost);
        canvas.addEventListener("webglcontextrestored", restored);
        cleanupRef.current = () => {
          canvas.removeEventListener("webglcontextlost", lost);
          canvas.removeEventListener("webglcontextrestored", restored);
          contextRef.current = null;
        };
      }}>
      <RoomLighting ambientHex={ambientHex}>
      <CameraRig view={view} />
      <SceneBoundary onError={fail}>
        <ModelLoaderScope
          url={url}
          treatment={treatment}
          trimId={trimId}
          ambientHex={ambientHex}
          onLoading={loading}
          primaryHex={primaryHex}
          secondaryHex={secondaryHex}
          threadHex={threadHex}
          trimHex={trimHex}
          steeringHex={steeringHex}
          accentHex={accentHex}
          cockpitBlackHex={cockpitBlackHex}
          onLoaded={loaded}
          onStats={stats}
        />
      </SceneBoundary>
      </RoomLighting>
    </Canvas>}
    {status !== "success" && <div className="absolute inset-x-4 bottom-4 z-10 rounded-[2px] bg-graphite px-3 py-2 text-xs text-paper"
      role="status" aria-live="polite" data-testid="viewer-status">
      {status === "loading" ? "Loading your interior…" : status === "empty" ? "3D model contains no geometry. Your selections are retained." : "3D preview unavailable (" + (error ?? "unknown error") + "). Your selections are retained."}
      {status !== "loading" && <button type="button" onClick={retry} className="ml-3 underline underline-offset-2">Retry 3D</button>}
    </div>}
  </div>;
}
