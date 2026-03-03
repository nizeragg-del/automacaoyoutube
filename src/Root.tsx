import "./index.css";
import { Composition, staticFile } from "remotion";
import { StoryComposition } from "./StoryComposition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="StoryVideo"
        component={StoryComposition as any}
        durationInFrames={1800} // 60 segundos por padrão
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          images: [staticFile("placeholder.jpg")], // Array de fallback
          text: "Qualquer história impactante cabe aqui. Teste do sistema.",
          audio: staticFile("placeholder_audio.mp3")
        }}
      />
    </>
  );
};
