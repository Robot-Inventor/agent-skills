import fs from "fs/promises";
import packageJson from "../package.json";
import pluginJson from "../.codex-plugin/plugin.json";

const main = async () => {
    pluginJson.version = packageJson.version;
    await fs.writeFile(".codex-plugin/plugin.json", JSON.stringify(pluginJson, null, 4));
};

await main();
