import { useParams, Link } from "react-router-dom";
import { useState, useEffect, useLayoutEffect } from "react";
import { useDispatch } from "react-redux";
import { callAPI } from "../utils/CallApi";
import { US_CURRENCY } from "../utils/constants";
import { ProductDetails, CarouselProduct } from "../components";
import { addToCart } from "../redux/cartSlice";

import * as API from "../api/serverApis.js";

const ProductPage = () => {
  const { id } = useParams();

  const [product, setProduct] = useState(null);
  const [products, setProducts] = useState(null);

  const [quantity, setQuantity] = useState("1");

  const dispatch = useDispatch();

  useEffect(() => {
    getProduct();
  }, []);

  const getProduct = () => {
    let data = {};
    API.product(id).then((searchResults) => {
      data = searchResults.data;
      API.productCarouselData(data).then((searchResult) => {
        const productList = searchResult.data;
        setProducts(productList);
      });
      setProduct(searchResults.data);
    });
  };

  if (localStorage.getItem("storedProducts") === null) {
    localStorage.setItem("storedProducts", "[]");
  }

  var storeProductsArray = JSON.parse(localStorage.getItem("storedProducts"));

  storeProductsArray.push(product);

  const addQuantityToProduct = () => {
    setProduct((product.quantity = quantity));
    return product;
  };

  if (!product?.product_name) return <h1>Loading Product ...</h1>;

  return (
    product && (
      <div className="bg-amazonclone-background">
        <div className="min-w-[1000px] max-w-[1500px] m-auto p-4">
          <div className="grid grid-cols-10 gap-2">
            {/* Left */}
            <div className="col-span-3 p-8 rounded bg-white m-auto">
              <img src={`${product.img_link}`} alt="" />
            </div>
            {/* Middle */}
            <div className="col-span-5 p-4 rounded bg-white divide-y divide-gray-400">
              <div className="mb-3">
                <ProductDetails product={product} ratings={true} />
              </div>
              <div className="text-base xl:text-lg mt-3">
                {product.product_description}
              </div>
            </div>
            {/* Right */}
            <div className="col-span-2 p-4 rounded bg-white">
              <div className="text-xl xl:text-2xl font-semibold text-red-700 text-right">
                {US_CURRENCY.format(product.price)}
              </div>
              {/* <div className="text-base xl:text-lg font-semibold text-gray-500 text-right">
                RRP:
                <span className="line-through">{US_CURRENCY.format(product.oldPrice)}</span>
              </div> */}
              <div className="text-sm xl:text-base font-semibold text-blue-500 mt-3">
                FREE Returns
              </div>
              <div className="text-sm xl:text-base font-semibold text-blue-500 mt-1">
                Free Delivery
              </div>
              <div className="text-base xl:text-lg font-semibold text-green-700 my-1">
                In Stock
              </div>
              <div className="text-base xl:text-lg">
                Quantity:
                <select
                  onChange={(e) => setQuantity(e.target.value)}
                  className="p-2 bg-white border rounded-md focus:border-indigo-600"
                >
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                </select>
              </div>
              <Link to={"/checkout"}>
                <button
                  onClick={() => dispatch(addToCart(addQuantityToProduct()))}
                  className="btn"
                >
                  Add to Cart
                </button>
              </Link>
            </div>
          </div>
        </div>
        <div className="min-w-[1000px] max-w-[1500px] m-auto p-4">
          <CarouselProduct
            products={products}
            carouselType="Similar Products You May Like"
          />
        </div>
      </div>
    )
  );
};

export default ProductPage;
