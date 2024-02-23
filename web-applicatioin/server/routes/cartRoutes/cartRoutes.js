import express from 'express'
import { getAllCartItems, getSingleCartItem, createCart, deleteSingleCartItem, updateSingleCartItem } from '../../controllers/cart.js';


const cartRouter = express.Router();

cartRouter.get("/cart", getAllCartItems);
cartRouter.get("/cart/:id", getSingleCartItem);
cartRouter.post("/cart", createCart);
cartRouter.put("/cart/:id", updateSingleCartItem);
cartRouter.delete("/cart/:id", deleteSingleCartItem);

export default cartRouter;