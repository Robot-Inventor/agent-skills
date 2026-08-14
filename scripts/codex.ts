import { exists, readFile } from "node:fs/promises";
import { dirname, join, parse } from "node:path";
import { SKILLS } from "./skills";

const main = async () => {
    let input = "";
    process.stdin.setEncoding("utf8");
    for await (const chunk of process.stdin) {
        input += chunk;
    }

    const { cwd } = JSON.parse(input) as { cwd: string };

    const isWebProject = await exists(join(cwd, "package.json"));
    const skills = isWebProject ? SKILLS.web : SKILLS.nonWeb;

    const pluginRoot = process.env.PLUGIN_ROOT;
    if (!pluginRoot) {
        throw new Error("PLUGIN_ROOT is not set");
    }

    const skillContentPromises = skills.map(async (skill) => {
        const skillPath = join(pluginRoot, "skills", skill, "SKILL.md");
        const skillContent = await readFile(skillPath, "utf8");

        return [`<forced-skill name="${skill}">`, skillContent, "</forced-skill>"].join("\n");
    });

    const skillContents = await Promise.all(skillContentPromises);
    const content = skillContents.join("\n\n");

    process.stdout.write(content);
};

await main();
