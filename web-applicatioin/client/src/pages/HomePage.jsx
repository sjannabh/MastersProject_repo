import React from "react";
import {
  Carousel,
  HomePageCard,
  CarouselCategory,
  CarouselProduct,
} from "../components";
import { useEffect, useState } from "react";

import * as API from "../api/serverApis.js";

const HomePage = () => {
  const [products, setProducts] = useState(null);

  const getSearchResults = () => {
    API.productsList("usb", 10).then((searchResults) => {
      const productList = searchResults.data;
      setProducts(productList);
      console.log("productList");
      console.log(products);
    });
  };

  useEffect(() => {
    getRecResults().then((product) => setProducts(product));
  }, []);

  const getRecResults = () => {
    const temp = fetch(API.productsList("usb", 10)); //.then((searchResults) => {
    //   const productList = searchResults.data;
    //setProducts(productList);
    console.log("temp");
    console.log(products);
    return temp;
  };

  return (
    <div className="bg-amazonclone-background">
      <div className="min-w-[1000px] max-w-[1500px] m-auto bg-white-400">
        <Carousel />
        <div className="grid grid-cols-3 xl:grid-clos-4 -mt-80">
          <HomePageCard
            title={"We have a surprize for you"}
            img={"../images/home_grid_1.jpg"}
            link={"See terms and conditions"}
          />
          <HomePageCard
            title={"Watch The Rings of Power"}
            img={"../images/home_grid_2.jpg"}
            link={"Start streaming now"}
          />
          <HomePageCard
            title={"Unlimited Streaming"}
            img={"../images/home_grid_3.jpg"}
            link={"Find out more"}
          />
          <HomePageCard
            title={"More titles to explore"}
            img={"../images/home_grid_4.jpg"}
            link={"Browse Kindly Unlimited"}
          />
          <HomePageCard
            title={"Shop Pet Supplies"}
            img={"../images/home_grid_5.jpg"}
            link={"See more"}
          />
          <HomePageCard
            title={"Spring Sale"}
            img={"../images/home_grid_6.jpg"}
            link={"See the deals"}
          />
          <HomePageCard
            title={"Echo Buds"}
            img={"../images/home_grid_7.jpg"}
            link={"See more"}
          />
          <HomePageCard
            title={"Family Plan: 3 months free"}
            img={"../images/home_grid_8.jpg"}
            link={"Learn more"}
          />
          <div className="m-3 pt-8">
            <img
              className="xl:hidden"
              src={"../images/banner_image_2.jpg"}
              alt=""
              // srcset=""
            />
          </div>
        </div>
        <CarouselProduct products={products} />
        <CarouselCategory />
        <div className="h-[200px]">
          <img
            className="h-[100%] m-auto"
            src={"../images/banner_image.jpg"}
            alt=""
          />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
