import { Button, Modal, Form } from "react-bootstrap";
import { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useGetBusMutation } from "../api/bus";

export const BusCreateModal = () => {
  const [show, setShow] = useState(false);

  const mutation = useGetBusMutation();

  const formik = useFormik({
    initialValues: {
      licence_plate: "",
    },
    validationSchema: Yup.object({
      licence_plate: Yup.string().max(10).required(),
    }),
    onSubmit: (values) => {
      mutation.mutate(values);
    },
  });

  return (
    <>
      <Button onClick={() => setShow(true)}>Add Bus</Button>

      <Modal show={show} onHide={() => setShow(false)}>
        <Form
          onSubmit={(e) => {
            e.preventDefault();
            formik.handleSubmit();
            setShow(false);
          }}
        >
          <Modal.Header closeButton>
            <Modal.Title>Add Bus</Modal.Title>
          </Modal.Header>

          <Modal.Body>
            <Form.Label htmlFor="licence_plate">Licence Plate</Form.Label>
            <Form.Control
              id="licence_plate"
              name="licence_plate"
              onChange={formik.handleChange}
              value={formik.values.licence_plate}
            />
            <Form.Control.Feedback type="invalid" className={"d-block"}>
              {formik.errors.licence_plate}
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
