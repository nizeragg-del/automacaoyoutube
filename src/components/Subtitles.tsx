import React, { useState, useEffect, useCallback, useMemo } from "react";
import {
    AbsoluteFill,
    staticFile,
    delayRender,
    continueRender,
    useCurrentFrame,
    useVideoConfig,
    interpolate,
    Easing
} from "remotion";
import { createTikTokStyleCaptions, Caption } from "@remotion/captions";

interface SubtitlesProps {
    audioFile: string;
    subtitles?: Caption[]; // Dados injetados diretamente via props
}

const HIGHLIGHT_COLOR = "#FFD700"; // Amarelo Ouro
const SWITCH_CAPTIONS_EVERY_MS = 1400; // Agrupa palavras

export const Subtitles: React.FC<SubtitlesProps> = ({ audioFile, subtitles }) => {
    const [captions, setCaptions] = useState<Caption[] | null>(subtitles || null);
    // Usamos delayRender diretamente para máxima compatibilidade entre versões de hooks
    const [handle] = useState(() => delayRender("loading-captions"));

    const { fps } = useVideoConfig();
    const frame = useCurrentFrame();

    const fetchCaptions = useCallback(async () => {
        // Se já temos as legendas via props, liberamos a renderização imediatamente
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
    const currentPage = pages.find(p => currentTimeMs >= p.startMs && currentTimeMs < p.endMs) || null;

    if (!currentPage) return null;

    return (
        <AbsoluteFill style={{
            justifyContent: "center",
            alignItems: "center",
            top: "15%",
            padding: "0 40px"
        }}>
            <div style={{
                fontSize: 68,
                fontWeight: 900,
                textAlign: "center",
                color: "white",
                textTransform: "uppercase",
                fontFamily: "Inter, sans-serif",
                textShadow: "0px 0px 15px rgba(0,0,0,0.8), 2px 2px 0px #000",
                display: "flex",
                flexWrap: "wrap",
                justifyContent: "center",
                gap: "12px",
                lineHeight: 1.1
            }}>
                {currentPage.tokens.map((token, i) => {
                    const isActive = currentTimeMs >= token.fromMs && currentTimeMs < token.toMs;
                    const scale = isActive ? 1.15 : 1;
                    const rotate = isActive ? (i % 2 === 0 ? 1 : -1) : 0;

                    return (
                        <span
                            key={`${token.fromMs}-${i}`}
                            style={{
                                color: isActive ? HIGHLIGHT_COLOR : "white",
                                display: "inline-block",
                                transform: `scale(${scale}) rotate(${rotate}deg)`,
                                transition: "transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
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
