import { BrowserRouter, Routes, Route } from "react-router-dom";

import { NavBar, CheckOut, SearchResults, } from "./components";
import HomePage from './pages/HomePage.jsx'
import ProductPage from './pages/ProductPage.jsx'
import Login from './pages/Login.jsx';
import SignUp from './pages/SignUp.jsx';



const App = () => {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route exact path="/" element={<HomePage />} />
        <Route exact path="/signup" element={<SignUp />} />
        <Route exact path="/login" element={<Login />} />
        <Route exact path="/signup" element={<SignUp />} />
        <Route exact path="/search" element={<SearchResults />} />
        <Route exact path="/product/:id" element={<ProductPage />} />
        <Route exact path="/checkout" element={<CheckOut />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
