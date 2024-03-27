import express from "express"; // this is to hit the express server
import mongoose from "mongoose";
import bodyParser from "body-parser"; // to process data sent in the HTTP request body
import cors from "cors"; // this cors acts as the middleware to access the api in the react front end from the backend
import userRoutes from "./routes/userRoutes/userRoutes.js";
import productRoutes from "./routes/productRoutes/productRoutes.js";
import reviewRoutes from "./routes/reviewRoutes/reviewRoutes.js";
import cartRoutes from "./routes/cartRoutes/cartRoutes.js";
import orderRoutes from "./routes/orderRoutes/orderRoutes.js";
import browsingHistoryRoutes from "./routes/browsingHistoryRoutes/browsingHistoryRoutes.js";
import endPoints from "express-list-endpoints";
import expressListRoutes from "express-list-routes";
import dotenv from "dotenv"

dotenv.config()

const database_connection_String = process.env.MONGO_DB_CONNECTION_STRING;

const app = express();
const port = 5000;
const serverUrl = `http://localhost:${port}`;

app.use(bodyParser.json());
app.use(cors());

app.use("/", userRoutes);
app.use("/", productRoutes);
app.use("/", reviewRoutes);
app.use("/", cartRoutes);
app.use("/", orderRoutes);
app.use("/", browsingHistoryRoutes);

mongoose
    .connect(database_connection_String)
    .then(console.log(`connected to the database`))
    .catch((error) => console.log(error));

app.get("/", (req, res) => {
    //expressListRoutes(app, { prefix: serverUrl });
    res.status(200).send(endPoints(app));
});

app.get("/health", (req, res) => res.send("ECommerce Express is and Running"));

app.all("*", (req, res) => res.status(404).json({ message: "Route doesn't exists. Please check the request" })); // if the route doen't exixts

app.listen(port, () => console.log(`Server is listening on port: ${serverUrl}`));
