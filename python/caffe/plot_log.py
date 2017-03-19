#!/usr/bin/env python
#coding=utf-8

import inspect
import os
import random
import sys
from parse_log import ParseTrain
from parse_log import ParseTest
import argparse
import matplotlib.pyplot as plt
import matplotlib.markers as mks


class PlotLog(object):

    def __init__(self, match_dict_list):
        self.description_separator_ = " vs. "
        self.key_list_ = match_dict_list[0].keys()
        self.convert_data(match_dict_list)
        self.create_fileds()
        self.create_chart_types()

    def convert_data(self, match_dict_list):
        self.match_list_dict_ = {}
        for key in self.key_list_:
            self.match_list_dict_[key] = []

        for line_dict in match_dict_list:
            if len(self.key_list_) != len(line_dict):
                print "The number of keys must be same! \n"
                sys.exit(1)
            for key in self.key_list_:
                self.match_list_dict_[key].append(line_dict[key])

    def create_fileds(self):
        self.x_axis_fields_ = ["iteration"]
        self.y_axis_fields_ = []
        for key in self.key_list_:
            if not key in self.x_axis_fields_:
                self.y_axis_fields_.append(key)

    def create_chart_types(self):
        self.chart_types_ = []
        for x_axis_field in self.x_axis_fields_:
            for y_axis_field in self.y_axis_fields_:
                self.chart_types_.append((x_axis_field, y_axis_field))

    def get_num_type(self):
        return len(self.chart_types_) 

    def get_chart_type(self, chart_id):
        if chart_id >= len(self.chart_types_) or chart_id < 0:
            print "chart_id = {} is not valid!".format(chart_id)
            sys.exit(1)
        return self.chart_types_[chart_id]

    def get_chart_id(self, chart_type):
        if not chart_type in self.chart_types_:
            print "chart_type = ({}, {}) is not suported!".format(chart_type[0], chart_type[1])
            sys.exit(1)
        for chart_id in range(len(self.chart_types_)):
            if self.chart_types_[chart_id] == chart_type:
                return chart_id 

    def get_chart_type_description(self, chart_id):
        x_axis_field, y_axis_field = self.get_chart_type(chart_id)
        return x_axis_field + self.description_separator_ + y_axis_field

    def get_chart_data(self, chart_type):
        x_axis_field, y_axis_field = chart_type
        return (self.match_list_dict_[x_axis_field], self.match_list_dict_[y_axis_field])

    def random_marker(self):
        markers = mks.MarkerStyle.markers
        num = len(markers.values())
        idx = random.randint(0, num - 1)
        return markers.values()[idx]

    def plot_chart(self, path_to_jpg, chart_id, use_marker, chart_label, legend_loc, linewidth):
        chart_type = self.get_chart_type(chart_id)
        chart_data = self.get_chart_data(chart_type)
        chart_color = [random.random(), random.random(), random.random()]
        # If there too many datapoints, do not use marker, so ser use_marker = False
        if not use_marker:
            plt.plot(chart_data[0], chart_data[1], label = chart_label, \
                color = chart_color, linewidth = linewidth)
        else:
            # Some markers throw ValueError: Unrecognized marker style
            is_ok = False

            while not is_ok:
                try:
                    chart_marker = self.random_marker()
                    plt.plot(chart_data[0], chart_data[1], label=chart_label, \
                        color=chart_color, marker=chart_marker, linewidth=linewidth)
                    is_ok = True
                except:
                    pass

        plt.rcParams['figure.figsize'] = (10, 10)        # large images
        plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
        plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap
        plt.legend(loc=legend_loc, ncol=1)
        plt.title(self.get_chart_type_description(chart_id))
        x_axis_field, y_axis_field = chart_type
        plt.xlabel(x_axis_field)
        plt.ylabel(y_axis_field)
        plt.savefig(path_to_jpg)
        plt.show()

    def print_chart_type(self, offset):
        print "chart_id\t\t\tchart_type\n"
        for chart_type in self.chart_types_:
            chart_id = self.get_chart_id(chart_type) + offset
            print "{}\t\t\t({}, {})\n".format(chart_id, chart_type[0], chart_type[1])

# End to define class PlotLog

class PlotALL(object):

    def __init__(self, train_plot, test_plot):
        self.train_plot_ = train_plot
        self.test_plot_ = test_plot
        self.create_id_type_dict()
    
    def create_id_type_dict(self):
        self.id_type_dict_ = {}
        id = 0
        for chart_type in self.train_plot_.chart_types_:
            self.id_type_dict_[id] = chart_type
            id += 1
        for chart_type in self.test_plot_.chart_types_:
            self.id_type_dict_[id] = chart_type
            id += 1

    def get_chart_type(self, chart_id):
        return self.id_type_dict_[chart_id]

    def get_mode_name(self, chart_id):
        if chart_id < len(self.train_plot_.chart_types_):
            return "train"
        else:
            return "test"

    def get_chart_data(self, chart_id):
        if chart_id < len(self.train_plot_.chart_types_):
            chart_type = self.get_chart_type(chart_id)
            return self.train_plot_.get_chart_data(chart_type)
        else:
            chart_type = self.get_chart_type(chart_id)
            return self.test_plot_.get_chart_data(chart_type)

    def random_marker(self):
        markers = mks.MarkerStyle.markers
        num = len(markers.values())
        idx = random.randint(0, num - 1)
        return markers.values()[idx]

    def print_chart_type(self):
        print "Train chart type!"
        print "chart_id\t\t\tchart_type\n"
        for chart_id, chart_type in self.id_type_dict_.items():
            if chart_id == len(self.train_plot_.chart_types_):
                print "Test chart type!"
                print "chart_id\t\t\tchart_type\n"
            print "{}\t\t\t({}, {})\n".format(chart_id, chart_type[0], chart_type[1])

    def plot_chart(self, path_to_jpg, chart_id_list, legend_loc, use_marker, linewidth):
        plt.rcParams['figure.figsize'] = (10, 10)        # large images
        plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
        plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap

        for chart_id in chart_id_list:
            chart_data = self.get_chart_data(chart_id)
            chart_type = self.get_chart_type(chart_id)
            y_axis_field = chart_type[1]
            chart_label = self.get_mode_name(chart_id) + y_axis_field
            chart_color = [random.random(), random.random(), random.random()]
            # If there too many datapoints, do not use marker, so ser use_marker = False
            if not use_marker:
                plt.plot(chart_data[0], chart_data[1], label = chart_label, \
                    color = chart_color, linewidth = linewidth)
            else:
            # Some markers throw ValueError: Unrecognized marker style
                is_ok = False

                while not is_ok:
                    try:
                        chart_marker = self.random_marker()
                        plt.plot(chart_data[0], chart_data[1], label=chart_label, \
                            color=chart_color, marker=chart_marker, linewidth=linewidth)
                        is_ok = True
                    except:
                        pass

            plt.legend(loc=legend_loc, ncol=1)
        # plt.title(self.get_chart_type_description(chart_id))
        # x_axis_field, y_axis_field = chart_type
        # plt.xlabel(x_axis_field)
        # plt.ylabel(y_axis_field)
        plt.savefig(path_to_jpg)
        plt.show()

def parse_args():
    """Plot chart to analysis training and testing state"""
    description = "Plot chart to analysis training and testing state!"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("log_file", help="Path to log")
    parser.add_argument("path_to_jpg", help="Directory to output a jpg image")
    parser.add_argument("--chart_id_list", action="store", type=int, nargs='*', default=None, help="Chart_id represents which type of charts to plot")
    parser.add_argument("--use_marker", action="store_true", help="Whether to use marker in the chart")
    parser.add_argument("--chart_label", action="store", type=str, default="chart label", help="Whether to use marker in the chart")
    parser.add_argument("--legend", action="store_true", help="Whether to put legend on upper right part of the chart")
    parser.add_argument("--linewidth", action="store", type=int, default=0.75, help="The width of line")
    # parser.add_argument("--plot_test", action="store_true", help="Whether to plot training or testing chart")
    parser.add_argument("--show_id", action="store_true", help="Whether to show chart id")
    args = parser.parse_args()
    return args

def absolute_path(output_dir):
    abs_path = None
    script_root = os.getcwd()
    if output_dir.find(".") == 0:
        abs_path = os.path.join(script_root, output_dir.strip("./"))
    elif output_dir.find("/") == 0:
        abs_path = output_dir
    else:
        abs_path = os.path.join(script_root, output_dir)
    return abs_path

def main():
    """Main method"""
    args = parse_args()
    log_file = args.log_file
    if not os.path.exists(log_file):
        print "Not found log_file {}".format(log_file)
        sys.exit(1)
    path_to_jpg = args.path_to_jpg
    path_to_jpg = absolute_path(path_to_jpg)
    jpg_root = os.path.dirname(path_to_jpg)
    if not os.path.exists(jpg_root):
        print "Not found jpg_root {}".format(jpg_root)
        sys.exit(1)
    
    use_marker = args.use_marker
    legend_loc = "upper right" if args.legend else "lower right"

    linewidth = args.linewidth
    if linewidth <= 0:
        print "linewidth must be positive!"
        sys.exit(1)

    parser_train = ParseTrain(log_file)
    parser_train.find_all_regex()
    plot_train = PlotLog(parser_train.match_dict_list)
    parser_test = ParseTest(log_file)
    parser_test.find_all_regex()
    plot_test = PlotLog(parser_test.match_dict_list)
    plot_all = PlotALL(plot_train, plot_test)
    if args.show_id:
        plot_all.print_chart_type()
        return

    chart_id_list = args.chart_id_list
    if len(chart_id_list) == 0:
        print "The length of chart_id_list can not be zero!"
        sys.exit(1)

    try:
        plot_all.plot_chart(path_to_jpg, chart_id_list, legend_loc, use_marker, linewidth)
    except:
        print "Fail to plot a train chart!"
        sys.exit(1)
if __name__ == '__main__':
    main()
