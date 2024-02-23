import express from "express"; // this is to hit the express server
import mongoose from "mongoose";
import bodyParser from "body-parser"; // to process data sent in the HTTP request body
import cors from "cors"; // this cors acts as the middleware to access the api in the react front end from the backend
import userRoutes from "./routes/userRoutes/userRoutes.js";
import productRoutes from "./routes/productRoutes/productRoutes.js";
import reviewRoutes from "./routes/reviewRoutes/reviewRoutes.js";
import cartRoutes from './routes/cartRoutes/cartRoutes.js';
import orderRoutes from './routes/orderRoutes/orderRoutes.js';
import browsingHistoryRoutes from './routes/browsingHistoryRoutes/browsingHistoryRoutes.js';


const database_connection_String = "mongodb+srv://qwerty:Qwerty123@myecomcluster.jqhkqxz.mongodb.net/?retryWrites=true&w=majority"

const app = express();
const port = 5000;

app.use(bodyParser.json());
app.use(cors())

app.use('/', userRoutes);
app.use('/', productRoutes);
app.use('/', reviewRoutes);
app.use('/', cartRoutes);
app.use('/', orderRoutes);
app.use('/', browsingHistoryRoutes);

mongoose.connect(database_connection_String)
    .then(console.log(`connected to the database`))
    .catch((error) => console.log(error));


app.get("/", (req, res) => res.send('Hello From Ecommerce Express'));

app.all('*', (req, res) => res.status(404).json({ message: "Route doesn't esists. Please check the request" })) // if the route doen't exixts

app.listen(port, () => console.log(`Server is listening on port: http://localhost:${port}`))
