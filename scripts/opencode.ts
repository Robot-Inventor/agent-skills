import type { Plugin } from "@opencode-ai/plugin";
import { SKILLS } from "./skills";
import { exists } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const plugin: Plugin = async ({ project, directory }) => {
    const isWebProject = await exists(join(directory, "package.json"));
    const skills = isWebProject ? SKILLS.web : SKILLS.nonWeb;

    return {
        config: async (config) => {
            config.instructions ??= [];

            for (const skill of skills) {
                const path = fileURLToPath(new URL(`../skills/${skill}/SKILL.md`, import.meta.url));

                if (!config.instructions.includes(path)) {
                    config.instructions.push(path);
                }
            }
        }
    };
};

export { plugin };
