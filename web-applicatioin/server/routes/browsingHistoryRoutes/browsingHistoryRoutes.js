import express from 'express'

import { createAndUpdateHistory, getBrowsingHistory } from '../../controllers/browsingHistory.js';

const browsingHistoryRoutes = express.Router();

browsingHistoryRoutes.get('/browsingHistory/:id', getBrowsingHistory);
browsingHistoryRoutes.post('/browsingHistory', createAndUpdateHistory);

export default browsingHistoryRoutes;