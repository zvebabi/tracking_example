import numpy as np
import cv2

from tracking_utils import visualization as vis

def plot_trajectory(image, trajectories, track_ids, path_lenght):
    canvas = image.copy()
    history_depth = {}
    for track_id in track_ids:
        if track_id in trajectories.keys():
            color = vis.get_color(int(track_id))
            if len(trajectories[track_id]) < 2:
                continue
            prev_tlwh = trajectories[track_id][-1]
            path_len_actual = 0
            history_depth[track_id] = 1
            for i, tlwh in reversed(list(enumerate(trajectories[track_id][:-1]))):
                x1, y1, w, h = tlwh
                x1_p, y1_p, w_p, h_p = prev_tlwh
                pt1 = (int(x1 + 0.5 * w), int(y1 + h))
                pt2 = (int(x1_p + 0.5 * w_p), int(y1_p + h_p))
                prev_tlwh = tlwh
                path_len_actual += np.linalg.norm( np.array(pt1) - np.array(pt2))
                if path_len_actual < path_lenght:
                    history_depth[track_id] += 1
                    cv2.line(canvas, pt1, pt2, color, thickness=2)
                    cv2.circle(canvas, pt1, 2, color, thickness=2)
                else:
                    break
    return canvas, history_depth

def plot_homography(image, trajectories, track_ids, path_lenght, frame):
    canvas = image.copy()
    homoGraphy = np.array([0.00467919462394561,-0.00106004410217054,-1.09720060345245,0.00963165705752871,-0.0706995954499526,8.52759538597223,0.000189291756286462,-0.000856961083763378,0.0301514423255732]).reshape((3,3))

    for track_id in track_ids:
        if track_id in trajectories.keys():
            color = vis.get_color(int(track_id))
            if len(trajectories[track_id]) < 2:
                continue
            pts = np.stack(trajectories[track_id][-path_lenght[track_id]:], axis=0)
            xy = np.zeros(shape=(pts.shape[0], 2))
            xy[:,0] = pts[:,0] + pts[:,2]/2
            xy[:,1] = pts[:,1] + pts[:,3]
            pts_on_gp = cv2.perspectiveTransform(xy[None, :, :], homoGraphy)[0,:,:]
            
            #supposed interpolation from gp to image plane(floor plan) pt * scale + shift, where scale = image_size/gp_size, and shift is pose of gp_origin in pixels coords
            ch, cw, _ = canvas.shape
            scale = np.array(((85-62)/(-4-3),(510-230)/(-68-57))) #supposed scale 
            # shift = np.array((ch/2,cw/2)) # supposed shift
            shift = np.array((73, 380)) # supposed shift
            pts_on_plan = pts_on_gp*scale + shift
            cv2.polylines(canvas, [pts_on_plan[:, [1,0]].astype('int32')], False, color, 2)
    return canvas
