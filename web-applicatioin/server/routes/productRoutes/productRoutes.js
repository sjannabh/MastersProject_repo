import express from "express";
import {
    getProducts,
    getProductsByName,
    createProduct,
    getProduct,
    deleteProduct,
    updateProduct,
} from "../../controllers/products.js";

const productRouter = express.Router();

productRouter.get("/products", getProducts);
productRouter.get("/products/:name/:count", getProductsByName);
productRouter.get("/product/:id", getProduct);
productRouter.post("/product", createProduct);
productRouter.put("/product/:id", updateProduct);
productRouter.delete("/product/:id", deleteProduct);

export default productRouter;
