import React from "react";
import {
    AbsoluteFill,
    Audio,
    Img,
    interpolate,
    useCurrentFrame,
    useVideoConfig,
    staticFile,
} from "remotion";
import { Subtitles } from "./components/Subtitles";
import { Caption } from "@remotion/captions";

interface StoryData {
    images: string[];
    text: string;
    audio: string;
    subtitles?: Caption[]; // Injeção direta via props
}

export const StoryComposition: React.FC<StoryData> = ({ images, text, audio, subtitles }) => {
    const frame = useCurrentFrame();
    const { durationInFrames, fps } = useVideoConfig();

    // Proteção de fallback para arrays vazios/indefinidos
    const validImages = Array.isArray(images) && images.length > 0 ? images : [""];

    // Calcula quantos frames cada imagem deve ficar na tela
    const framesPerImage = durationInFrames / validImages.length;
    const transitionFrames = fps * 1.5; // Transição suave

    return (
        <AbsoluteFill style={{ backgroundColor: "black" }}>

            {validImages.map((src, index) => {
                const startFrame = index * framesPerImage;
                const endFrame = startFrame + framesPerImage + (index < validImages.length - 1 ? transitionFrames : 0);

                if (frame < startFrame || frame > endFrame) {
                    return null;
                }

                const scale = interpolate(frame, [startFrame, endFrame], [1, 1.18], {
                    extrapolateRight: "clamp",
                    extrapolateLeft: "clamp"
                });

                const panMod = index % 2 === 0 ? 1 : -1;
                const panX = interpolate(frame, [startFrame, endFrame], [-18 * panMod, 18 * panMod]);
                const panY = interpolate(frame, [startFrame, endFrame], [-10 * panMod, 10 * panMod]);

                let opacity = interpolate(frame, [startFrame, startFrame + transitionFrames], [0, 1], {
                    extrapolateRight: "clamp", extrapolateLeft: "clamp"
                });

                if (index < validImages.length - 1) {
                    const fadeOutStart = endFrame - transitionFrames;
                    const opacityOut = interpolate(frame, [fadeOutStart, endFrame], [1, 0], {
                        extrapolateRight: "clamp", extrapolateLeft: "clamp"
                    });
                    opacity = Math.min(opacity, opacityOut);
                }

                return (
                    <AbsoluteFill
                        key={`scene-${index}`}
                        style={{
                            transform: `scale(${scale}) translate(${panX}px, ${panY}px)`,
                            opacity,
                            zIndex: index
                        }}
                    >
                        {src && (
                            <Img
                                src={src.startsWith("http") ? src : staticFile(src)}
                                style={{
                                    width: "100%",
                                    height: "100%",
                                    objectFit: "cover",
                                }}
                            />
                        )}
                    </AbsoluteFill>
                );
            })}

            {/* Legendas Dinâmicas Sincronizadas */}
            <Subtitles audioFile={audio} subtitles={subtitles} />

            {/* Headline (Título) */}
            <AbsoluteFill style={{
                top: "8%",
                height: "15%",
                justifyContent: "center",
                alignItems: "center",
                padding: "0 50px"
            }}>
                <h1 style={{
                    color: "white",
                    fontSize: 48,
                    fontWeight: 900,
                    textTransform: "uppercase",
                    textAlign: "center",
                    fontFamily: "Inter, sans-serif",
                    textShadow: "0px 4px 10px rgba(0,0,0,0.9), 2px 2px 0px #000",
                    margin: 0,
                    letterSpacing: "1px"
                }}>
                    {text}
                </h1>
            </AbsoluteFill>

            {/* Efeito de Grain / Ruído */}
            <AbsoluteFill
                style={{
                    backgroundColor: "transparent",
                    backgroundImage: `url("https://www.transparenttextures.com/patterns/real-carbon-fibre.png")`,
                    opacity: 0.08,
                    mixBlendMode: "overlay",
                    pointerEvents: "none",
                    zIndex: validImages.length + 5
                }}
            />

            {/* Vinheta */}
            <AbsoluteFill
                style={{
                    background: "radial-gradient(circle, rgba(0,0,0,0) 35%, rgba(0,0,0,0.85) 100%)",
                    zIndex: validImages.length + 10,
                    pointerEvents: "none"
                }}
            />

            <Audio src={audio.startsWith("http") ? audio : staticFile(audio)} />
        </AbsoluteFill>
    );
};
