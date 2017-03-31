import math
from matplotlib import pyplot as plt
import numpy as np  # np.append(some_array, column, axis=1) appends a column to array
import pylab
from scipy.fftpack import fft, ifft, fftfreq
from skimage.transform import iradon

from matplotlib import pyplot as plt
from scipy import misc

MAX_ANGLE = 360

class SinogramLogic:
    def __init__(self, image, alpha, detectors_amount, cone_width):
        self.image = image
        self.alpha = float(alpha)
        self.detectors_amount = int(detectors_amount)
        self.cone_width = int(cone_width)
        self.sinogram = np.zeros((self.detectors_amount, 1))
        self.result_image = np.zeros(self.image.shape)

    def plotEmitersAndDecoders(self, x, y, iks, igrek, detectors_x_list, detectors_y_list):
        plt.scatter(iks, igrek, color="red")
        plt.scatter(detectors_x_list, detectors_y_list, color="blue")
        circle = plt.Circle([x / 2, y / 2], radius=x / 2, fill=False, color='green')
        for (x2, y2) in zip(detectors_x_list, detectors_y_list):
            plt.plot([iks, x2], [igrek, y2], color='gray', linestyle='dashed', linewidth=2)

    def computeSinogram(self, image, alpha, progress, detectors_amount, cone_width):
        x, y = image.shape
        angle = 0
        sinogram = np.zeros((detectors_amount, 1))
        # print("computeSinogram")
        #for angle in range(0, 180+self.alpha, self.alpha):
        while angle < MAX_ANGLE*progress+alpha:
            sums = list()
            detectors_x_list = list()
            detectors_y_list = list()
            emiter_x = x/2 - x/2*math.cos(math.radians(angle))
            emiter_y = y/2 - y/2*math.sin(math.radians(angle))
            #print(str(emiter_x) + " " + str(emiter_y) + " dla " + str(angle) + " stopni")
            for detector in range(detectors_amount):
                det_x = x / 2 - x / 2 * math.cos(
                     math.radians(angle + 180 - cone_width / 2 + detector * cone_width / (detectors_amount - 1)))
                det_y = y / 2 - y / 2 * math.sin(
                    math.radians(angle + 180 - cone_width / 2 + detector * cone_width / (detectors_amount - 1)))
                detectors_x_list.append(det_x)
                detectors_y_list.append(det_y)
                # print(str(det_x) + " " + str(det_y) + " detektor numer " + str(detector))
                sums.append(self.bresenhamComputeSum(int(emiter_x), int(emiter_y), int(det_x), int(det_y)))
            if angle == 0:
                sinogram[:, 0] = list(sums)
            else:
                temp = np.zeros((detectors_amount, 1))
                temp[:, 0] = list(sums)
                sinogram = np.append(sinogram, temp, axis=1)
            angle += alpha
            # self.plotEmitersAndDecoders(x, y, emiter_x, emiter_y, detectors_x_list, detectors_y_list)
        return sinogram

    def plot_sinogram(self, sinogram):
        plt.imshow(sinogram*1.0/np.max(sinogram)*255, cmap="gray")
        plt.savefig('foo.png')

    def bresenhamComputeSum(self, x_start, y_start, x_end, y_end):
        x = x_start
        y = y_start
        limity = self.image.shape[0] - 1
        limitx = self.image.shape[1] - 1
        if x_start < x_end:
            xi = 1
            dx = x_end - x_start
        else:
            xi = -1
            dx = x_start - x_end
        if y_start < y_end:
            yi = 1
            dy = y_end - y_start
        else:
            yi = -1
            dy = y_start - y_end
        sumOfPixels = int(self.image[min(limity, y)][min(limitx, x)])
        if dx > dy:
            ai = (dy - dx) * 2
            bi = dy * 2
            d = bi - dx
            while not x == int(x_end):
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    x += xi
                # print(self.image[y - 1][x - 1])
                sumOfPixels += int(self.image[min(limity, y)][min(limitx, x)])
        else:
            ai = (dx - dy) * 2
            bi = dx * 2
            d = bi - dy
            while not y == int(y_end):
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    y += yi
                #print(self.image[y-1][x-1])
                sumOfPixels += int(self.image[min(limity, y)][min(limitx, x)])
        return sumOfPixels  # sum of brightnesses of pixels on a line between emiter and chosen decoder

    def pixels_in_line(self, x_start, y_start, x_end, y_end):
        pixels = []
        x = x_start
        y = y_start
        limit = self.image.shape[0] - 1
        if x_start < x_end:
            xi = 1
            dx = x_end - x_start
        else:
            xi = -1
            dx = x_start - x_end
        if y_start < y_end:
            yi = 1
            dy = y_end - y_start
        else:
            yi = -1
            dy = y_start - y_end
        if dx > dy:
            ai = (dy - dx) * 2
            bi = dy * 2
            d = bi - dx
            while not x == int(x_end):
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    x += xi
                pixels.append((x-1, y-1))
        else:
            ai = (dx - dy) * 2
            bi = dx * 2
            d = bi - dy
            while not y == int(y_end):
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    y += yi
                pixels.append((x-1, y-1))
        return pixels

    def color_pixels(self, summ, pixels):
        for coords in pixels:
            self.result_image[coords[0]][coords[1]] += summ/len(pixels)

    def normalize(self, image):
        amin = np.min(image)
        amax = np.max(image)
        return (image-amin)/(amax - amin)
                
    def plot_result(self, result):
        plt.imshow(self.normalize(result)*255, cmap="gray")
        plt.savefig('result.png')

    def inverse_radon(self, sinogram, output_image_size, alpha, progress, detectors_amount, cone_width):
        x, y = output_image_size
        for emiter_index, angle in enumerate(range(0, int(MAX_ANGLE*progress+alpha), int(alpha))):
            sums = list()
            detectors_x_list = list()
            detectors_y_list = list()
            emiter_x = x/2 - x/2*math.cos(math.radians(angle))
            emiter_y = y/2 - y/2*math.sin(math.radians(angle))
            for detector_index, detector in enumerate(range(detectors_amount)):
                det_x = x / 2 - x / 2 * math.cos(
                    math.radians(angle + 180 - cone_width / 2 + detector * cone_width / (detectors_amount - 1)))
                det_y = y / 2 - y / 2 * math.sin(
                    math.radians(angle + 180 - cone_width / 2 + detector * cone_width / (detectors_amount - 1)))
                detectors_x_list.append(det_x)
                detectors_y_list.append(det_y)
                # print(str(det_x) + " " + str(det_y) + " detektor numer " + str(detector))
                self.color_pixels(sinogram[detector_index, emiter_index],
                                  self.pixels_in_line(int(emiter_x), int(emiter_y), int(det_x), int(det_y)))
                # print(emiter_index, detector_index)
        return self.result_image

    def compute_mse(self, input_image, output_image):
        suma = 0
        for input_pixel, output_pixel in zip(np.nditer(self.normalize(input_image)), np.nditer(self.normalize(output_image))):
            #print(input_pixel)
            suma += (input_pixel - output_pixel)**2
        # print(suma)
        return suma/input_image.size

    def make_computations(self, image, alpha, progress, detectors_amount, cone_width):
        sg = self.computeSinogram(image, alpha, progress, detectors_amount, cone_width)
        invsg = self.inverse_radon(sg, image.shape, alpha, progress, detectors_amount, cone_width)
        return self.compute_mse(image, invsg)

    def make_computations2(self):
        sg = self.computeSinogram(self.image, self.alpha, 1, self.detectors_amount, self.cone_width)
        invsg = self.inverse_radon(sg, self.image.shape, self.alpha, 1, self.detectors_amount, self.cone_width)
        return self.compute_mse(image, invsg)

    def image_processing(self, image, alpha, progress, detectors_amount, cone_width):
        sg = self.computeSinogram(image, alpha, progress, detectors_amount, cone_width)
        invsg = self.inverse_radon(sg, image.shape, alpha, progress, detectors_amount, cone_width)
        filtered = self.filter(invsg, 5)
        return sg, filtered

    def filter2(self, image, window_width):
        output = np.zeros(image.shape)

        for j in range(image.shape[1]):
            for i in range(image.shape[0]):
                gain = 0
                for window_index in range((-window_width//2), (window_width//2)):
                    real_window_element_index = i + window_index
                    if real_window_element_index >= 0 and real_window_element_index < image.shape[0]:
                        if window_index == 0:
                            gain += image[real_window_element_index][j] 
                        elif window_index%2 == 0:
                            gain -= 4/math.pi**2/window_index**2*image[real_window_element_index][j]
                output[i][j] += gain
        return output

    def filter(self, image, window_width):
        output = np.zeros(image.shape)

        for j in range(image.shape[1]):
            for i in range(image.shape[0]):
                gain = 0
                for window_index in range((-window_width//2), (window_width//2)):
                    real_window_element_index = i + window_index
                    if real_window_element_index >= 0 and real_window_element_index < image.shape[0]:
                        
                        if window_index == 0:
                            gain += image[real_window_element_index][j] 
                        elif window_index%2 == 0:
                            gain += image[real_window_element_index][j] * 0.5
                        elif window_index%3 == 0:
                            gain += image[real_window_element_index][j] * 0.25
                output[i][j] += gain
        return output


    def alpha_comparison(self, image):
        min_alpha = 1
        max_alpha = 90
        step = 5
        detectors_amount = 20
        cone_width = 120
        return [[alpha, self.make_computations(image, alpha, 1, detectors_amount, cone_width)] for alpha in range(min_alpha, max_alpha, step)]

    def detectors_amount_comparison(self, image):
        min_detectors_amount = 5
        max_detectors_amount = 100
        step = 5
        alpha = 5
        cone_width = 180
        return [[detectors_amount, self.make_computations(image, alpha, 1, detectors_amount, cone_width)] for detectors_amount in range(min_detectors_amount, max_detectors_amount, step)]
    
    def cone_width_comparison(self, image):
        detectors_amount = 100
        step = 5
        alpha = 5
        min_cone_width = 5
        max_cone_width = 100
        return [[cone_width, self.make_computations(image, alpha, 1, detectors_amount, cone_width)] for cone_width in range(min_cone_width, max_cone_width, step)]


    def mse_iterations(image):
        mses = []
        alphas = [1]
        alphas.extend(list(range(5, 91, 5)))
        print(alphas)
        for alpha in alphas:
            print(alpha)
            sinogram = SinogramLogic(image, alpha, 100, 150)
            mses.append([alpha, 360/alpha, sinogram.make_computations2()])
        return mses

    def filter_comparison(self, image):
        detectors_amount = 30
        min_window_width = 4
        max_window_width = 50
        step = 2

        alpha = 5
        cone_width = 90

        return [self.make_filter_computations(image, alpha, 1, detectors_amount, cone_width, window_width) for window_width in range(min_window_width, max_window_width, step)]
        
    def make_filter_computations(self, image, alpha, progress, detectors_amount, cone_width, window_width):
        sg = self.computeSinogram(image, alpha, progress, detectors_amount, cone_width)
        invsg = self.inverse_radon(sg, image.shape, alpha, progress, detectors_amount, cone_width)
        filtered = self.filter(invsg, window_width)
        return self.compute_mse(sg, invsg)-self.compute_mse(sg, filtered)

    def detectors_amount_plot(self, image):
        data = self.detectors_amount_comparison(image)
        x_axis = []
        y_axis = []

        for element in data:
            x_axis.append(element[0])
            y_axis.append(element[1])
        
        plt.plot(x_axis, y_axis, color="blue", marker="v")
        plt.title("Zależność błędu średniokwadratowego od liczby detektorów")
        plt.xlabel("Liczba detektorów")
        plt.ylabel("Błąd średniokwadratowy")
        plt.savefig("detectors_amount.pdf")

    def alpha_plot(self, image):
        data = self.alpha_comparison(image)
        x_axis = []
        y_axis = []

        for element in data:
            x_axis.append(element[0])
            y_axis.append(element[1])
        
        plt.plot(x_axis, y_axis, color="blue", marker="v")
        plt.title("Zależność błędu średniokwadratowego od kąta alfa")
        plt.xlabel("Kąt alfa")
        plt.ylabel("Błąd średniokwadratowy")
        plt.savefig("alpha.pdf")

    def cone_width_plot(self, image):
        data = self.cone_width_comparison(image)
        x_axis = []
        y_axis = []

        for element in data:
            x_axis.append(element[0])
            y_axis.append(element[1])
        
        plt.plot(x_axis, y_axis, color="blue", marker="v")
        plt.title("Zależność błędu średniokwadratowego od rozpiętości kątowej")
        plt.xlabel("Rozpiętość kątowa")
        plt.ylabel("Błąd średniokwadratowy")
        plt.savefig("cone_width.pdf")

    

if __name__ == "__main__":
    
    filename = 'images/tomograf-zdjecia/Kwadraty2.jpg'
    image = misc.imread(filename, mode="L")
    sinogram = SinogramLogic(image, 1, 300, 90)

    sinogram.detectors_amount_plot(image)

