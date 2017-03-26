import datetime
import time
import dicom as dcm
from dicom.dataset import Dataset, FileDataset
import numpy as np
from scipy import misc


def save_to_dicom_file(numpy_image, filename, patient_name, patient_id, patient_sex, comment, date_of_photo, time_of_photo):
        """
        :param numpy_image: 2d array with image to be saved
        :param filename: name of output file
        :param patient_name: patient's name
        :param patient_id: id of this patient
        :param patient_sex: sex of patient
        :param comment:
        :param date_of_photo: string with date in format 'YYYYMMDD'
        :param time_of_photo: time 'HH:MM PM/AM'
        :return:
        """
        print("Filling the meta data")
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage UID from DICOM standard
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # random UID (SOP - Service-Object Pair ) - UID of this dataset
        file_meta.ImplementationClassUID = "1.2.3.4"  # random UID - implementation that wrote this file
        ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)
        ds.ContentDate = date_of_photo
        ds.ContentTime = time_of_photo
        ds.PatientName = patient_name
        ds.PatientID = patient_id
        ds.PatientSex = patient_sex
        ds.TextComments = comment  # commentary about this photo
        # below we have data about the image,
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0
        ds.HighBit = 15
        ds.BitsStored = 16
        ds.BitsAllocated = 16  # we save the file as monochrome, 16-bit image
        ds.SmallestImagePixelValue = b'\\x00\\x00'
        ds.LargestImagePixelValue = b'\\xff\\xff'
        ds.Columns = numpy_image.shape[0]
        ds.Rows = numpy_image.shape[1]
        if numpy_image.dtype != np.uint16:
            numpy_image = numpy_image.astype(np.uint16)
        ds.PixelData = numpy_image.tostring()
        ds.save_as(filename)
        return

if __name__ == "__main__":
    pixel_array = misc.imread('/home/sefir/Dokumenty/IwM/Tomograf/CTScan/images/tomograf-zdjecia/Kropka.jpg', mode="L")#, flatten=True) <- IMAGE IN 8bit greyscale
    save_to_dicom_file(pixel_array, 'dicol.dcm', 'S^Frl', '12345', 'M', 'Weird^science', '20170322', '161023.12543')
