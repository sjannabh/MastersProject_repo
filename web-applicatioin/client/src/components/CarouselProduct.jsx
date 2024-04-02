import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation } from "swiper/modules";
import { Link } from "react-router-dom";
import TextTruncate from "react-text-truncate";
import "swiper/css";
import "swiper/css/navigation";

//api
// import * as API from "../api/serverApis.js";

// let products = API.productsList

const CarouselProduct = ({ products, carouselType }) => {
  return (
    <div>
      <div className="text-2xl font-semibold p-3">{carouselType}</div>
      <div className="bg-white m-3 p-3">
        <Swiper
          slidesPerView={7}
          spaceBetween={10}
          navigation={true}
          modules={[Navigation]}
        >
          {products &&
            products.map((product, key) => {
              return (
                <SwiperSlide key={key}>
                  <Link key={key} to={`/product/${product.product_id}`}>
                    <img
                      className="m-auto"
                      src={product.img_link}
                      alt="Recommend products"
                    />
                  </Link>
                  <TextTruncate
                    line={1}
                    element="span"
                    truncateText="…"
                    text={product.product_name}
                  />
                  {/* <p>{product.product_name}</p> */}
                  <p>Rating: {product.rating}</p>
                </SwiperSlide>
              );
            })}
        </Swiper>
      </div>
    </div>
  );
};

export default CarouselProduct;
