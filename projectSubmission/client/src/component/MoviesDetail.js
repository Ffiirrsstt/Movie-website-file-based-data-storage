import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState, useContext } from "react";
import MyContext from "../Context/MyContext";
import axios from "axios";
import Nav from "./Nav";
import "../css/MoviesDetail.css";

const MoviesDetail = () => {
  const [dataDetail, setDataDetail] = useState();
  const { readData } = useContext(MyContext);
  const { idMovies } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    readDataResult();
  }, []);

  const readDataResult = async () => {
    const resultData = await readData(true);
    if (!resultData[0]) return navigate(resultData[1]);

    axios
      .get(`${process.env.REACT_APP_API}movies/detail`, {
        params: {
          index: idMovies,
          username: resultData[1].username,
        },
      })
      .then((response) => {
        setDataDetail(JSON.parse(response.data));
      })
      .catch((error) => {});
  };

  return (
    <div className="vw-100 vh-100 bg-dark d-flex justify-content-center">
      <Nav />
      {dataDetail && (
        <div className="box-movies-detail d-flex justify-content-center align-items-center">
          <div className=" d-flex align-items-center h-80 w-100 text-white">
            <div className="d-flex h-100">
              <img
                src={dataDetail.image}
                alt={dataDetail.title}
                className="img-fluid rounded vw-40 h-100"
              />
            </div>
            <div className="h-100 w-100 d-flex flex-column align-items-center">
              <div className="w-80 h-50 d-flex flex-column pt-1vw pl-1 pr-1 pt-2">
                <h1 className="fs-4 h-100 mb-0 d-flex align-items-center">
                  {dataDetail.title}
                </h1>
                <h3 className="fs-6 text-secondary">
                  The number of viewers : {dataDetail.views.toLocaleString()}
                </h3>
                <div className="d-flex flex-wrap w-100 mt-1">
                  {dataDetail.keywords.split(" ").map((data, index) => (
                    <button
                      key={index}
                      className={`d-flex
                      fs-6 key-detail btn-info btn mb-1
                       ${
                         index === dataDetail.keywords.split(" ").length - 1
                           ? ""
                           : "mr-1"
                       }`}
                    >
                      <h3 className="fs-6 h-100">{data}</h3>
                      {/* <h3 className="fs-6 bg-success">{data}</h3> */}
                    </button>
                  ))}
                </div>

                <h3 className="fs-6 ">
                  Formats of shows: : {dataDetail.formats}
                </h3>
                <h3 className="fs-6 ">
                  Categories of shows. : {dataDetail.genres}
                </h3>
                <div>
                  <h4 className="fs-6 bg-briefly rounded mt-1 mb-1 p-3 vh-15">
                    Content summary : Updating information shortly.
                  </h4>
                </div>
              </div>
              <div className="h-50 w-80 d-flex flex-column justify-content-end pl-1 pr-1 pb-2">
                <div className="d-flex w-100 vh-12 mb-5">
                  <button className="w-100 h-100 bg-red btn bg-wg mr-1 ">
                    <h4 className="fs-5 ">First episode : 0</h4>
                  </button>
                  <button className="w-100 h-100 bg-red btn bg-wg">
                    <h4 className="fs-5">Latest episode : 0</h4>
                  </button>
                </div>
                <div className="d-flex justify-centent-between align-items-center w-100">
                  <h5 className="w-50 mr-1">Total number of episodes</h5>
                  <h5 className="pr-2 pl-2 h-25px m-0 text-end bg-wg text-dark rounded">
                    0
                  </h5>
                  <h5 className="ml-1 w-25 text-end">episodes</h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MoviesDetail;
