import { useContext, useState } from "react";
import axios from "axios";
import swal from "sweetalert";
import LoginRegister from "./LoginRegister";
import MyContext from "../Context/MyContext";

const Register = () => {
  const { messageError } = useContext(MyContext);
  const [userData, setUserData] = useState("");
  const [passwordData, setPasswordData] = useState("");

  const sendData = async () => {
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API}register`,
        { userData, passwordData }
      );
      const message = response.data.message;
      if (message) swal("Operation successful.", message, "success");
    } catch {
      messageError();
    }
  };

  const checkUser = async () => {
    try {
      const dataUsername = userData;
      const response = await axios.get(
        `${process.env.REACT_APP_API}register/User`,
        { params: { dataUsername } }
      );
      return response.data.resultCheck;
    } catch {
      messageError();
    }
  };

  const handleSubmit = async (event) => {
    try {
      event.preventDefault();
      const resultCheck = await checkUser();
      if (userData.replace(/ /g, "") !== "") {
        if (resultCheck) {
          if (passwordData.replace(/ /g, "") !== "") {
            await sendData();
          } else
            swal("Invalid password.", "Please enter your password.", "error");
        } else {
          swal(
            "The username is already in use.",
            "Please edit the username and proceed with registration again.",
            "error"
          );
        }
      } else {
        swal(
          "The username has an error.",
          "Edit the username without using special characters and without leaving any spaces.",
          "error"
        );
      }
    } catch {
      messageError();
    }
  };

  const receiveUserData = (data) => setUserData(data);
  const receivePassword = (data) => setPasswordData(data);

  return (
    <>
      <LoginRegister
        heading={"Sign Up"}
        textBtn={"Register"}
        textLink={"Click to go to the login page."}
        linkUrl={"/login"}
        sendUserData={receiveUserData}
        sendPassword={receivePassword}
        handleSubmit={handleSubmit}
      />
    </>
  );
};

export default Register;
