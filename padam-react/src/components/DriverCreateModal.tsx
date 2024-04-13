import { Button, Modal, Form } from "react-bootstrap";
import { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useGetDriversMutation } from "../api/driver";

export const DriverCreateModal = () => {
  const [show, setShow] = useState(false);

  const mutation = useGetDriversMutation();

  const formik = useFormik({
    initialValues: {
      username: "",
    },
    validationSchema: Yup.object({
      username: Yup.string().max(10).required(),
    }),
    onSubmit: (values) => {
      mutation.mutate(values);
    },
  });

  return (
    <>
      <Button onClick={() => setShow(true)}>Add Driver</Button>

      <Modal show={show} onHide={() => setShow(false)}>
        <Form
          onSubmit={(e) => {
            e.preventDefault();
            formik.handleSubmit();
            setShow(false);
          }}
        >
          <Modal.Header closeButton>
            <Modal.Title>Add Driver</Modal.Title>
          </Modal.Header>

          <Modal.Body>
            <Form.Label htmlFor="username">Drivers name</Form.Label>
            <Form.Control
              id="username"
              name="username"
              onChange={formik.handleChange}
              value={formik.values.username}
            />
            <Form.Control.Feedback type="invalid" className={"d-block"}>
              {formik.errors.username}
            </Form.Control.Feedback>
          </Modal.Body>
          <Modal.Footer>
            <Button type="submit" disabled={!formik.isValid}>
              Submit
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
};
