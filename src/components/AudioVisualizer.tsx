import React from "react";
import { useWindowedAudioData, visualizeAudio } from "@remotion/media-utils";
import { useCurrentFrame, useVideoConfig } from "remotion";

interface AudioVisualizerProps {
    audioSrc: string;
}

export const AudioVisualizer: React.FC<AudioVisualizerProps> = ({ audioSrc }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();

    const audioData = useWindowedAudioData({
        src: audioSrc,
        frame,
        fps,
        windowInSeconds: 0.1,
    });

    if (!audioData || !audioData.audioData) {
        return null;
    }

    const frequencies = visualizeAudio({
        fps,
        frame,
        audioData: audioData.audioData,
        numberOfSamples: 64, // Enough for a clean look
    });

    // We only use the first half of frequencies (bass/mids) as they are more visually interesting
    const limitedFrequencies = frequencies.slice(0, 32);

    return (
        <div style={{
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "center",
            height: 120,
            gap: 4,
            width: "80%",
            margin: "0 auto",
            position: "absolute",
            bottom: "10%",
            left: "10%",
            zIndex: 100,
        }}>
            {limitedFrequencies.map((v, i) => (
                <div
                    key={i}
                    style={{
                        flex: 1,
                        height: `${Math.max(5, v * 100)}%`,
                        backgroundColor: "#FFD700",
                        borderRadius: "2px",
                        boxShadow: "0 0 10px rgba(255, 215, 0, 0.5)",
                        opacity: 0.8,
                    }}
                />
            ))}
        </div>
    );
};
