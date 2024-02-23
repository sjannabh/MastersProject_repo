import { StarIcon } from "@heroicons/react/24/outline";

const ProductRatings = (props) => {
  const startNumber = props.avgRating;
  const ratingNumber = props.ratings;

  return (
    <div className="flex">
      {Array.from({ length: startNumber }, (_, i) => (
        <StarIcon
          key={i}
          className="stroke-[#F1B61F] fill-[#F1B61F] h-[20px]"
        />
      ))}
      {Array.from({ length: 5 - startNumber }, (_, i) => (
        <StarIcon key={i} className="stroke-[#F1B61F] [#F1B61F] h-[20px]" />
      ))}
      <span className="ml-3 text-blue-500">{ratingNumber} ratings</span>
    </div>
  );
};

export default ProductRatings;
