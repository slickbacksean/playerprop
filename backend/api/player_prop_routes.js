// player_props_routes.js
const express = require('express');
const router = express.Router();
const PredictionService = require('../services/prediction_service');
const authMiddleware = require('../auth/jwt_middleware');

router.get('/predict/:playerId', authMiddleware, async (req, res) => {
    try {
        const predictions = await PredictionService.getPrediction(req.params.playerId);
        res.json(predictions);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});