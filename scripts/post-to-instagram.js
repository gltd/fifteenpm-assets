import IgApiClient from "instagram-private-api";
import readFile from "fs";
import promisify from "util";

const readFileAsync = promisify(readFile);

const ig = new IgApiClient();

async function login() {
  // basic login-procedure
  ig.state.generateDevice(process.env.IG_USERNAME);
  await ig.account.login(process.env.IG_USERNAME, process.env.IG_PASSWORD);
}

(async () => {
  await login();

  const videoPath =
    "/var/folders/yq/9w62vkz95tq6x35c2lmgv0fm0000gn/T/tmpimsiozse.mp4";
  const coverPath =
    "/var/folders/yq/9w62vkz95tq6x35c2lmgv0fm0000gn/T/tmpv20ho4zv.png";

  const publishResult = await ig.publish.video({
    // read the file into a Buffer
    video: await readFileAsync(videoPath),
    coverImage: await readFileAsync(coverPath),
    caption: "hello world"
  });

  console.log(publishResult);
})();
