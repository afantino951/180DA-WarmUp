import cv2
from sklearn.cluster import KMeans


def main():
    
    cap = cv2.VideoCapture(0)
    frame_w  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
    frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
    rect_width = 100
    rect_height = 100

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        x_rect = [
            int((frame_w/2) - (rect_width/2)),
            int((frame_w/2) + (rect_width/2))
            ]
        y_rect = [
            int((frame_h/2) - (rect_height/2)), 
            int((frame_h/2) + (rect_height/2))
            ]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        rgb_cut = rgb[x_rect[0]:x_rect[1], y_rect[0]:y_rect[1], :]
        rgb_cut = rgb_cut.reshape((rgb_cut.shape[0] * rgb_cut.shape[1],3)) #represent as row*column,channel number
        clt = KMeans(n_clusters=2) #cluster number
        clt.fit(rgb_cut)

        color = clt.cluster_centers_.astype("uint8").tolist()[0]
        color.reverse()

        cv2.rectangle(frame,(x_rect[0],y_rect[0]),(x_rect[1],y_rect[1]),color,5)

        # Display the resulting frames
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()