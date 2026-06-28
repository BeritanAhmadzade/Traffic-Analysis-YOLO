
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon


img = cv2.imread("IMG_20260608_233848_316.jpg")
plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
plt.axis("off")

model = YOLO("yolov8x-world.pt")

print(img.shape)


results = model("IMG_20260608_233848_316.jpg",
                imgsz = 1280,
                conf = 0.1,
                verbose = True)


annotated = results[0].plot()
plt.figure(figsize=(9,9))
plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()


plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.grid()
plt.show()


ROI ={
    "top_roi":Polygon([(420,0),   (820,0),   (820,380),  (420,380)]),
    "bottom_roi":Polygon([(350,840), (850,840), (850,1200),  (350,1200)  ]),
    "right_roi":Polygon([(870,430), (1200,430),   (1200,700),    (870,700)]),
    "left_roi":Polygon([(0,430),   (330,430), (330,900),  (0,900)])
}


#vehicle_centers

def get_vehicles_center(results):
    centers = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        if model.names[cls]  not in ["car", "truck"]:
             continue
        x1,y1,x2,y2 = box.xyxy[0]
        cx = float((x1+x2)/2)
        cy = float((y1+y2)/2)
        centers.append((cx,cy))

    return centers 

#count in ROI
def count_cars(get_vehicles_center,roi):
    count = 0
    for cx,cy in get_vehicles_center:
        if roi.contains(Point(cx,cy)):
            count+=1

    return count   

#count all vehicles 
vehicles_center = get_vehicles_center(results)

print("total_cars :", len(vehicles_center))


#count cars in top ROI
top_count=count_cars(vehicles_center,ROI["top_roi"])
print("top_roi :",top_count)


# Count cars in each ROI
for roi_name, roi_poly in ROI.items():
    count = count_cars(vehicles_center, roi_poly)
    print (f"{roi_name}:{count}")

