import Joi from "joi";

const LoginSchema = Joi.object({
  username: Joi.string().required().messages({
    "string.empty": "Please field value.",
  }),
  password: Joi.string().min(8).max(200).required().messages({
    "string.empty": "Please field value.",
    "string.max": "Input max 200",
    "string.min": "Input much more than 8",
  }),
});
export { LoginSchema };
