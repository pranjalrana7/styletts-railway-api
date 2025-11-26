const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/create-video', upload.fields([{ name: 'images' }, { name: 'audio' }]), (req, res) => {
  const images = req.files['images'].map(f => f.path);
  const audio = req.files['audio'][0].path;

  const cmd = `ffmpeg -y -framerate 1/3 -i ${images.join(' -i ')} -i ${audio} -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4`;

  exec(cmd, (err) => {
    if (err) return res.status(500).send(err.toString());
    res.download('output.mp4');
  });
});

app.listen(process.env.PORT || 3000, () => console.log('FFmpeg API running'));
