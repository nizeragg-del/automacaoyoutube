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

interface StoryData {
    images: string[];
    text: string;
    audio: string;
}

export const StoryComposition: React.FC<StoryData> = ({ images, text, audio }) => {
    const frame = useCurrentFrame();
    const { durationInFrames, fps } = useVideoConfig();

    // Proteção de fallback para arrays vazios/indefinidos por versão legado
    const validImages = Array.isArray(images) && images.length > 0 ? images : [""];

    // Calcula quantos frames cada imagem deve ficar na tela, distribuindo o tempo
    const framesPerImage = durationInFrames / validImages.length;
    // Duração do Crossfade (transição)
    const transitionFrames = fps * 1.5; // 1.5 Segundos de transição suave

    return (
        <AbsoluteFill style={{ backgroundColor: "black" }}>

            {validImages.map((src, index) => {
                // Cálculo de tempo de cada cena (Atrasado + Duração)
                const startFrame = index * framesPerImage;
                // Cada cena estende um pouco na próxima para o crossfade acontecer
                const endFrame = startFrame + framesPerImage + (index < validImages.length - 1 ? transitionFrames : 0);

                // Se a cabeça de leitura (CurrentFrame) estiver fora dos limites + sobra de transição, não renderiza
                if (frame < startFrame || frame > endFrame) {
                    return null;
                }

                // 1. Efeito de Ken Burns (Zoom e Pan suave por cena)
                // Usando o start/end da cena específica, o Ken Burns reinicia pra cada imagem nova
                const scale = interpolate(frame, [startFrame, endFrame], [1, 1.18], {
                    extrapolateRight: "clamp",
                    extrapolateLeft: "clamp"
                });

                // Movimento de Pan intercalado (Cena par move esq/dir, Cena ímpar move dir/esq)
                const panMod = index % 2 === 0 ? 1 : -1;
                const panX = interpolate(frame, [startFrame, endFrame], [-18 * panMod, 18 * panMod]);
                const panY = interpolate(frame, [startFrame, endFrame], [-10 * panMod, 10 * panMod]);

                // 2. Crossfade 
                // Entrada da cena atual
                let opacity = interpolate(frame, [startFrame, startFrame + transitionFrames], [0, 1], {
                    extrapolateRight: "clamp", extrapolateLeft: "clamp"
                });

                // A 1ª cena não tem fade_in de outra imagem, mas vamos deixá-la vir do escuro
                // Saída (FadeOut) dessa mesma cena durante a transição com a próxima
                if (index < validImages.length - 1) {
                    const fadeOutStart = endFrame - transitionFrames;
                    const opacityOut = interpolate(frame, [fadeOutStart, endFrame], [1, 0], {
                        extrapolateRight: "clamp", extrapolateLeft: "clamp"
                    });
                    // O valor mestre da opacidade da cena desce no fim, enquanto a de cima sobe
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

            {/* Legendas Dinâmicas Sincronizadas (Sobre as imagens e vinheta) */}
            <Subtitles audioFile={audio} />

            {/* Headline (Título) no topo para retenção imediata */}
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

            {/* Efeito de Grain (Ruído Cinemático) para textura premium */}
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

            {/* Vinheta Estilizada (Cinemática) Escurece a tela ao redor como Cinema */}
            <AbsoluteFill
                style={{
                    background: "radial-gradient(circle, rgba(0,0,0,0) 35%, rgba(0,0,0,0.85) 100%)",
                    zIndex: validImages.length + 10, // Sempre acima de tudo, exceto talvez grão se quiser
                    pointerEvents: "none"
                }}
            />

            <Audio src={audio.startsWith("http") ? audio : staticFile(audio)} />
        </AbsoluteFill>
    );
};
