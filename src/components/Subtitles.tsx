import React, { useState, useEffect, useCallback, useMemo } from "react";
import {
    AbsoluteFill,
    staticFile,
    delayRender,
    continueRender,
    useCurrentFrame,
    useVideoConfig,
    spring,
} from "remotion";
import { createTikTokStyleCaptions, Caption } from "@remotion/captions";

interface SubtitlesProps {
    audioFile: string;
    subtitles?: Caption[];
}

const HIGHLIGHT_COLOR = "#FFD700"; // Amarelo Ouro
const HIGHLIGHT_BG = "rgba(0, 0, 0, 0.85)"; // Fundo preto semi-transparente para melhor leitura
const SWITCH_CAPTIONS_EVERY_MS = 250; // Reduzido drasticamente para evitar acúmulo de palavras

export const Subtitles: React.FC<SubtitlesProps> = ({ audioFile, subtitles }) => {
    const [captions, setCaptions] = useState<Caption[] | null>(subtitles || null);
    const [handle] = useState(() => delayRender("loading-captions"));

    const { fps } = useVideoConfig();
    const frame = useCurrentFrame();

    const fetchCaptions = useCallback(async () => {
        if (subtitles) {
            continueRender(handle);
            return;
        }

        try {
            const jsonFile = audioFile.replace(".mp3", ".json");
            const response = await fetch(staticFile(jsonFile));
            const data = await response.json();
            setCaptions(data);
        } catch (e) {
            console.error("Erro ao carregar legendas via fetch:", e);
        } finally {
            continueRender(handle);
        }
    }, [audioFile, handle, subtitles]);

    useEffect(() => {
        fetchCaptions();
    }, [fetchCaptions]);

    const { pages } = useMemo(() => {
        if (!captions) return { pages: [] };
        return createTikTokStyleCaptions({
            captions,
            combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
        });
    }, [captions]);

    if (!captions || pages.length === 0) return null;

    const currentTimeMs = (frame / fps) * 1000;
    const currentPage = pages.find(p => currentTimeMs >= p.startMs && currentTimeMs < p.startMs + p.durationMs) || null;

    if (!currentPage) return null;

    return (
        <AbsoluteFill style={{
            justifyContent: "center",
            alignItems: "center",
            top: "35%", // Movido mais para baixo para não cobrir o rosto
            height: "30%", // Limita a área vertical das legendas
            padding: "0 80px"
        }}>
            <div style={{
                fontSize: 84, // Aumentado para impacto, mas em menos palavras
                fontWeight: 900,
                textAlign: "center",
                color: "white",
                textTransform: "uppercase",
                fontFamily: "Inter, sans-serif",
                display: "flex",
                flexWrap: "wrap",
                justifyContent: "center",
                gap: "20px",
                lineHeight: 1.05
            }}>
                {currentPage.tokens.map((token, i) => {
                    const isActive = currentTimeMs >= token.fromMs && currentTimeMs < token.toMs;

                    // Spring pop animation
                    const scale = spring({
                        frame: (currentTimeMs - token.fromMs) * (fps / 1000),
                        fps,
                        config: { damping: 10, stiffness: 200 },
                    });

                    return (
                        <span
                            key={`${token.fromMs}-${i}`}
                            style={{
                                color: isActive ? HIGHLIGHT_COLOR : "white",
                                display: "inline-block",
                                transform: `scale(${isActive ? 1 + scale * 0.12 : 1})`,
                                backgroundColor: isActive ? HIGHLIGHT_BG : "transparent",
                                padding: "4px 16px",
                                borderRadius: "12px",
                                boxShadow: isActive ? "0px 15px 40px rgba(0,0,0,0.6)" : "none",
                                textShadow: isActive ? "none" : "0px 0px 20px rgba(0,0,0,0.9), 3px 3px 0px #000",
                            }}
                        >
                            {token.text}
                        </span>
                    );
                })}
            </div>
        </AbsoluteFill>
    );
};
