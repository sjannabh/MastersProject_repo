import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation } from "swiper/modules";
import { Link } from "react-router-dom";

import "swiper/css";
import "swiper/css/navigation";

//api
// import * as API from "../api/serverApis.js";

// let products = API.productsList

const CarouselProduct = (products) => {
  return (
    <div className="bg-white m-3">
      <div className="text-2xl font-semibold p-3">Best Sellers</div>
      <Swiper
        slidesPerView={7}
        spaceBetween={10}
        navigation={true}
        modules={[Navigation]}
      >
        {/* {products &&
          products.map((product,key) => {
            return (
              <SwiperSlide key={key}>
                <Link key={key} to={`/product/${product.product_id}`}>
                  <img
                    className="m-auto"
                    src={product.img_link}
                    alt="Recommend products"
                  />
                </Link>
                <p>Name</p>
                <p>Rating: 4.5</p>
              </SwiperSlide>
            );
          })} */}
      </Swiper>
    </div>
  );
};

export default CarouselProduct;
//  {
//    products &&
//      products.map((product, key) => {
//        return (
//          <SwiperSlide key={key}>
//            <Link key={key} to={`/product/${product.product_id}`}>
//              <img
//                className="m-auto"
//                src={product.img_link}
//                alt="Recommend products"
//              />
//            </Link>
//            <p>Name</p>
//            <p>Rating: 4.5</p>
//          </SwiperSlide>
//        );
//      });
//  }
