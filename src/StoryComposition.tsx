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

interface StoryData {
    image: string;
    text: string;
    audio: string;
}

export const StoryComposition: React.FC<StoryData> = ({ image, text, audio }) => {
    const frame = useCurrentFrame();
    const { durationInFrames } = useVideoConfig();

    // 1. Efeito de Zoom e Pan (Ken Burns)
    // Escala e movimento sutil ao longo do vídeo
    const scale = interpolate(frame, [0, durationInFrames], [1, 1.15], {
        extrapolateRight: "clamp",
    });

    // Movimento de Pan sutil (de -2% a 2% do tamanho)
    const panX = interpolate(frame, [0, durationInFrames], [-20, 20]);
    const panY = interpolate(frame, [0, durationInFrames], [-10, 10]);

    // 2. Efeito de Tremor (Câmera na mão)
    const shakeX = Math.sin(frame / 6) * 1.5;
    const shakeY = Math.cos(frame / 8) * 1.5;

    // 3. Fade In e Vinheta
    const opacity = interpolate(frame, [0, 45], [0, 1], {
        extrapolateRight: "clamp",
    });

    return (
        <AbsoluteFill style={{ backgroundColor: "black" }}>
            {/* Imagem com Zoom/Pan/Shake */}
            <AbsoluteFill
                style={{
                    transform: `scale(${scale}) translate(${panX + shakeX}px, ${panY + shakeY}px)`,
                    opacity,
                }}
            >
                <Img
                    src={image.startsWith("http") ? image : staticFile(image)}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                    }}
                />
            </AbsoluteFill>

            {/* Vinheta Estilizada (Cinemática) */}
            <AbsoluteFill
                style={{
                    background: "radial-gradient(circle, rgba(0,0,0,0) 40%, rgba(0,0,0,0.7) 100%)",
                }}
            />

            <Audio src={audio.startsWith("http") ? audio : staticFile(audio)} />
        </AbsoluteFill>
    );
};
