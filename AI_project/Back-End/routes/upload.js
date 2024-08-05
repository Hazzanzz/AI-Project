const express = require('express');
const multer = require('multer');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const router = express.Router();

// Set up multer for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});
const upload = multer({ storage: storage });

router.post('/upload', upload.single('sketch'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    const filePath = path.join(__dirname, '../', req.file.path);

    try {
        // Send the uploaded file to the AI model API
        const modelResponse = await axios.post('http://localhost:5000/api/generate-portrait', {
            sketchPath: filePath
        });

        // Get the URL of the generated portrait from the model response
        const portraitUrl = modelResponse.data.portraitUrl;

        res.json({ portraitUrl });
    } catch (error) {
        console.error('Error processing the sketch:', error);
        res.status(500).json({ error: 'Failed to process the sketch' });
    }
});

module.exports = router;
