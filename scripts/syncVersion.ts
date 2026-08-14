import fs from "fs/promises";
import packageJson from "../package.json";
import pluginJson from "../plugin.json";

const main = async () => {
  pluginJson.version = packageJson.version;
  await fs.writeFile("plugin.json", JSON.stringify(pluginJson, null, 4));
};

await main();
