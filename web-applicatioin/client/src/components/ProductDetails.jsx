import { ProductBadge, ProductRatings } from "./";
//import { useState, useEffect } from "react";

const ProductDetails = ({ product, ratings }) => {
  // var storedProductsArray = JSON.parse(
  //   localStorage.getItem("storedProducts") || "[]"
  // );

  // var storedProducts = {
  //   productsKey: product,
  //   dateKey: Date,
  // };

  // if (product.length !== 0) {
  //   storedProductsArray.push(storedProducts);
  // }

  // useEffect(() => {
  //   localStorage.setItem("product", JSON.stringify(storedProducts));
  // },[...storedProducts])

  return (
    <div className="mb-1">
      <div className="text-xl xl:text-2xl font-medium mb-1">
        {product.title}
      </div>
      <div className="text-sm xl:text-base mb-1">
        <span className="text-blue-500">{product.brand}</span>
      </div>
      {ratings && (
        <div className="text-sm xl:text-base mb-1">
          <ProductRatings
            avgRating={product.avgRating}
            ratings={product.ratings}
          />
        </div>
      )}
      <div className="text-xs xl:text-sm font-bold mb-1">
        {product.attribute}
      </div>
      <div>
        <ProductBadge badge={product.badge} />
      </div>
    </div>
  );
};

export default ProductDetails;
