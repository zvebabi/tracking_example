from opts import opts

class opts_v2(opts):
    def __init__(self):
        super().__init__()
        self.parser.add_argument('--track_history', type=int, default=100,
                        help='Length of the object path in pixels. Default 100.')
        self.parser.add_argument('--topview_path', type=str, default="",
                        help='Path to image with foolr plan')
