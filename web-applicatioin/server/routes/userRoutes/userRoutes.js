import express from 'express'
import { getUsers, createUser, getUser, deleteUser, updateUser, userSignin } from '../../controllers/users.js';


const userRouter = express.Router();

userRouter.get("/users", getUsers);
userRouter.get("/user/:id", getUser);
userRouter.post("/user", createUser);
userRouter.post("/user/signin", userSignin);
userRouter.put("/user/:id", updateUser);
userRouter.delete("/user/:id", deleteUser);

export default userRouter;