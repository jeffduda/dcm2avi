import itk
import numpy as np
import cv2
import argparse
import sys

def dcm2avi(dcm_path, avi_path):
    """
    Convert 3D dicom US to avi

    Args:
        dcm_path (str): Path to dicom
        avi_path (str): Path to output avi file

    """

    try:
        img = itk.imread(dcm_path)
    except Exception as e:
        raise Exception(f"Error loading input file: {e}")

    fps=10
    if img.GetMetaDataDictionary().HasKey("0018|0040"):
        fps = int(img.GetMetaDataDictionary()["0018|0040"])
    
    n_frames,height,width,n_channel = img.shape
    arr = itk.GetArrayViewFromImage(img)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(avi_path, fourcc, fps, (width, height), isColor=True)

    for i in range(n_frames):
        frame = arr[i,:,:,:]
        out.write(frame)
    
    out.release()

def main():
    parser = argparse.ArgumentParser(description='Apply lung segmentation models to a CT volume')
    parser.add_argument('-i', '--input', help='Input CT volume', type=str, required=True)
    parser.add_argument('-o', '--output', help='Output avi file', required=True)
    #parser.add_argument('-f', '--frames_per_second', help='Frames per second', type=int, default=10)
    args = parser.parse_args()

    dcm2avi(args.input, args.output)

if __name__=="__main__":
    sys.exit(main())