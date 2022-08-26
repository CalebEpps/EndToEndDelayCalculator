import matplotlib
import matplotlib.pyplot as plt
import sys


class End2EndCalculation:

    # configurable parameters
    def __init__(self, message_size=16000, init_segment_size=4, trans_speed=4000, segmentation_slices=6):
        self.trans_speed = trans_speed
        self.init_packet_size = message_size / init_segment_size
        self.message_size = message_size
        self.segmentation_sizes = []
        # method that allows configurable number of segmentations
        self.init_sizes(segmentation_slices)
        self.e2e_delays = []

    # get Initial Sizes and save them to list
    def init_sizes(self, segmentation_slices):
        temp_size = self.init_packet_size
        for x in range(segmentation_slices):
            self.segmentation_sizes.append(int(temp_size))
            temp_size /= 2

    # Void function; calculates the end-to-end delay
    def calculate_delay(self, num_links=3, overhead=0):
        print("------------------------")
        print("CURRENT OVERHEAD IS: ", overhead)
        print("------------------------")

        for i in range(len(self.segmentation_sizes)):
            trans_delay = ((self.segmentation_sizes[i] + overhead) / self.init_packet_size)
            N = self.message_size / self.segmentation_sizes[i]
            e2e = (num_links * trans_delay) + ((N - 1) * trans_delay)
            self.e2e_delays.append(e2e)
            # Final Organized Printout
            print("Packet Size: ".rjust(10) + str(self.segmentation_sizes[i]).rjust(10) +
                  "     End to End Delay: ".rjust(10) + "%.2f".rjust(10) % e2e)

        print("\n")

    # Function can be safely ignored, only used to generate necessary plots

    def display_Plots(self):
        plt = matplotlib.pyplot

        self.calculate_delay()
        plt.plot(self.segmentation_sizes, self.e2e_delays, label="Overhead: 0 Bits", color="blue")

        self.e2e_delays.clear()
        self.calculate_delay(overhead=10)
        plt.plot(self.segmentation_sizes, self.e2e_delays, label="Overhead: 10 Bits", color="red")

        self.e2e_delays.clear()
        self.calculate_delay(overhead=20)
        plt.plot(self.segmentation_sizes, self.e2e_delays, label="Overhead: 20 Bits", color="purple")

        plt.title("Message Segmentation Demonstration")
        plt.xlabel("Bits in Packet")
        plt.ylabel("Time in Seconds")

        plt.legend()

        plt.gca().invert_xaxis()
        # plt.gca().set_xscale('log')

        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())

        plt.show()


if __name__ == "__main__":
    print("\nWithout a command line argument in the form of a number,")
    print("the program will default to the 3 overhead values required")
    print("for the assignment.")

    e2e = End2EndCalculation()

    if len(sys.argv) == 2:
        input_overhead = int(sys.argv[1])
        e2e.calculate_delay(overhead=input_overhead)
        # Uncomment proceeding lines to show graph for end-to-end delay
        plt.plot(e2e.segmentation_sizes, e2e.e2e_delays, label="Overhead: " + str(input_overhead) + " Bits",
                 color="purple")

        plt.title("Message Segmentation Demonstration")
        plt.xlabel("Bits in Packet")
        plt.ylabel("Time in Seconds")

        plt.legend()

        plt.gca().invert_xaxis()
        plt.xlim([e2e.segmentation_sizes[0], e2e.segmentation_sizes[len(e2e.segmentation_sizes) - 1]])

        plt.show()

    # On error (No system args), the program will display the assignment-specific values.
    else:
        e2e.display_Plots()
