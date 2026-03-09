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
const HIGHLIGHT_BG = "#000000"; // Preto para contraste
const SWITCH_CAPTIONS_EVERY_MS = 1400;

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
            top: "20%",
            padding: "0 60px"
        }}>
            <div style={{
                fontSize: 72,
                fontWeight: 900,
                textAlign: "center",
                color: "white",
                textTransform: "uppercase",
                fontFamily: "Inter, sans-serif",
                display: "flex",
                flexWrap: "wrap",
                justifyContent: "center",
                gap: "18px",
                lineHeight: 1.1
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
                                transform: `scale(${isActive ? 1 + scale * 0.15 : 1})`,
                                backgroundColor: isActive ? HIGHLIGHT_BG : "transparent",
                                padding: "0 12px",
                                borderRadius: "8px",
                                boxShadow: isActive ? "0px 10px 30px rgba(0,0,0,0.5)" : "none",
                                textShadow: isActive ? "none" : "0px 0px 15px rgba(0,0,0,0.8), 2px 2px 0px #000",
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
