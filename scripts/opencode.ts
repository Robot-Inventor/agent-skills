import { Plugin } from "@opencode/plugin";
import type { PluginModule } from "@opencode-ai/plugin";
import { SKILLS } from "./skills";
import { exists, readFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const selectSkills = async (directory: string) =>
    (await exists(join(directory, "package.json"))) ? SKILLS.web : SKILLS.nonWeb;

const skillPath = (skill: string) => fileURLToPath(new URL(`../skills/${skill}/SKILL.md`, import.meta.url));

const plugin = {
    ...Plugin.define({
        id: "io.roboin.agent-skills",
        async setup(ctx) {
            const skills = await selectSkills(ctx.location.directory);
            const instructions = await Promise.all(skills.map((skill) => readFile(skillPath(skill), "utf8")));

            await ctx.session.hook("context", (event) => {
                for (const text of instructions) {
                    event.system.push({ type: "text", text });
                }
            });
        }
    }),
    async server({ directory }) {
        const skills = await selectSkills(directory);

        return {
            config: async (config) => {
                config.instructions ??= [];

                for (const skill of skills) {
                    const path = skillPath(skill);

                    if (!config.instructions.includes(path)) {
                        config.instructions.push(path);
                    }
                }
            }
        };
    }
} as const satisfies PluginModule;

export default plugin;
