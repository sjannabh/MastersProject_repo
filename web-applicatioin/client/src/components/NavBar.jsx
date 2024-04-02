import { useEffect, useState } from "react";
import { ShoppingCartIcon } from "@heroicons/react/24/outline";
import { Search } from "./";
import { useSelector } from "react-redux";

import { Link, Navigate } from "react-router-dom";

const NavBar = () => {
  // const [loggedUser, setLoggedUser] = useState("");

  // useEffect(() => {
  //   setLoggedUser(localStorage.getItem("fname"));
  // }, []);

  const handleClick = () => {
    localStorage.setItem("user", null);
    localStorage.setItem("authenticated", false);
    <Navigate to="/" />;
    window.location.reload();
  };

  //const{user_name} = useSelector((state) => state.user)

  // useEffect(() => {
  //   const loggedInUser = JSON.parse(localStorage.getItem("fname"));
  //   console.log(loggedInUser);
  //   if (loggedInUser) {
  //     <Navigate replace to="/" />;
  //   }
  // }, []);

  // const displayUserName = () => {

  //   <Navigate replace to="/" />;
  //   // JSON.parse(localStorage.getItem("fname"));
  // };

  const cart = useSelector((state) => state.cart.productsNumber);

  return (
    <header className="min-w-[1000px]">
      <div className="flex bg-amazonclone text-white h-[60px]">
        {/* Left */}
        <div className="flex items-center m-4">
          <Link to={"/"}>
            <img
              className="h-[35px] w-[100px] m-2"
              src={"../images/amazon.png"}
              alt=""
            />
          </Link>
          <div className="pr-4 pl-4">
            <div className="text-xs xl:text-sm">Deliver to</div>
            <div className="text-sm xl:text-base font-bold">United Kingdom</div>
          </div>
        </div>

        {/* Middle */}
        <div className="flex grow relative">
          <Search />
        </div>

        {/* Right */}
        <div className="flex items-center m-4">
          <div className="pr-4 pl-4">
            {localStorage.getItem("authenticated") === "true" ? (
              <div className="text-sm xl:text-sm">
                Hello, {JSON.parse(localStorage.getItem("user")).fname}
              </div>
            ) : (
              <div className="text-sm xl:text-sm">
                {/* Hello, */}
                {/* <Link to="/login"> Sign In</Link> */}
              </div>
            )}
            <div className="text-sm xl:text-base font-bold">
              Accounts & Lists
            </div>
          </div>
          <div className="pr-4 pl-4">
            {localStorage.getItem("authenticated") === "true" ? (
              <button className="text-sm xl:text-sm" onClick={handleClick}>
                Sign Out
              </button>
            ) : (
              <div className="text-sm xl:text-sm">
                <Link to="/login">Sign in</Link>
              </div>
            )}
          </div>
          <Link to={"/checkout"}>
            <div className="flex pr-3 pl-3">
              <ShoppingCartIcon className="h-[48px]" />
              <div className="relative">
                <div className="absolute right=[12px] font-bold m-2 text-orange-400">
                  {cart}
                </div>
              </div>
              <div className="mt-7 text-xs xl:text-sm font-bold">Cart</div>
            </div>
          </Link>
        </div>
      </div>
      <div className="flex bg-amazonclone-light_blue text-white space-x-3 text-xs xl:text-sm p-2 pl-6">
        <div>Today's Deals</div>
        <div>Customer Service</div>
        <div>TRegistry</div>
        <div>Gift Cards</div>
        <div>Sell</div>
      </div>
    </header>
  );
};

export default NavBar;
