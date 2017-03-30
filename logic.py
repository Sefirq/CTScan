import math
from matplotlib import pyplot as plt
import numpy as np  # np.append(some_array, column, axis=1) appends a column to array
import pylab
from scipy.fftpack import fft, ifft, fftfreq
from skimage.transform import iradon

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
        # ax = plt.gca()
        # ax.set_xlim(-1, x + 1)
        # ax.set_ylim(-1, y + 1)
        # ax.imshow(self.image, cmap='gray')
        # ax.add_artist(circle)
        # plt.show()

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
               
        # ax = plt.gca()
        # plt.show()
        # pylab.show()

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
        #print("---------")
        #print(sumOfPixels)
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
    
    # def lightness_value_for_pixels(self, sum, pixels):
    #     filter = False
        
    #     if filter:
    #         return [sum/len(pixels) for pixel in pixels]
    #     else:
            

    def color_pixels(self, summ, pixels):
        filter = True
        if filter:
            for i, coords in enumerate(pixels):
                for j, coords2 in enumerate(pixels):
                    k = abs(j-i)
                    gain = 0
                    if k==0:
                        gain = summ/len(pixels)
                    elif k%2==1:    
                        gain = -4/math.pi**2/k**2*(summ/len(pixels))
                    self.result_image[coords[0]][coords[1]] += gain
        else:
            for coords in pixels:
                self.result_image[coords[0]][coords[1]] += summ/len(pixels)
                

    def plot_result(self, result):
        plt.imshow(result*1.0/np.max(result)*255, cmap="gray")
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
                print(emiter_index, detector_index)
        return self.result_image

    def compute_mse(self, input_image, output_image):
        sum = 0
        for input_pixel, output_pixel in zip(np.nditer(input_image), np.nditer(output_image)):
            #print(input_pixel)
            sum += (input_pixel - output_pixel)**2
        
        return sum/input_image.size

    def make_computations(self, image, alpha, progress, detectors_amount, cone_width):
        sg = self.computeSinogram(image, alpha, progress, detectors_amount, cone_width)
        invsg = self.inverse_radon(sg, image.shape, alpha, progress, detectors_amount, cone_width)
        return self.compute_mse(image, invsg)

    def image_processing(self, image, alpha, progress, detectors_amount, cone_width):
        sg = self.computeSinogram(image, alpha, progress, detectors_amount, cone_width)
        invsg = self.inverse_radon(sg, image.shape, alpha, progress, detectors_amount, cone_width)
        return (sg, invsg)


    def alpha_comparison(self, image):
        min_alpha = 5
        max_alpha = 90
        step = 5
        detectors_amount = 5
        cone_width = 10
        return [self.make_computations(image, alpha, 1,detectors_amount, cone_width) for alpha in range(min_alpha, max_alpha, step)]

    def detectors_amount_comparison(self, image):
        min_detectors_amount = 1
        max_detectors_amount = 20
        step = 1
        alpha = 5
        cone_width = 10
        return [self.make_computations(image, alpha, 1, detectors_amount, cone_width) for detectors_amount in range(min_detectors_amount, max_detectors_amount, step)]
    
    def cone_width_comparison(self, image):
        detectors_amount = 5
        step = 1
        alpha = 5
        min_cone_width = 1
        max_cone_width = 50
        return [self.make_computations(image, alpha, 1, detectors_amount, cone_width) for cone_width in range(min_cone_width, max_cone_width, step)]

from scipy import misc
filename = 'images/tomograf-zdjecia/Kwadraty2.jpg'
image = misc.imread(filename, mode="L")
sinogram = SinogramLogic(image, 1, 30, 150)
progress=1
sg = sinogram.computeSinogram(image, sinogram.alpha, progress, sinogram.detectors_amount, sinogram.cone_width)
sinogram.plot_sinogram(sg)
invsg = sinogram.inverse_radon(sg, image.shape, sinogram.alpha, progress, sinogram.detectors_amount, sinogram.cone_width)
# filtered = sinogram.fbp(invsg, sinogram.alpha)
# filtered = sinogram.scikit_iradon(sg)
sinogram.plot_result(invsg)


mse = sinogram.compute_mse(image, invsg)
