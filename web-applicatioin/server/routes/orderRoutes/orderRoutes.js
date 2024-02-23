import express from 'express'
import { getAllOrders, getSingleOrder, updateOrder, deleteOrder } from '../../controllers/orders.js'


const orderRouter = express.Router();

orderRouter.get('/orders', getAllOrders);
orderRouter.get('/order/:id', getSingleOrder);
orderRouter.put('/order/:id', updateOrder);
orderRouter.delete('/order/:id', deleteOrder);


export default orderRouter
