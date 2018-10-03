from .InputExtractor import InputExtractor
import numpy as np

# Encapsulates a sub-dataset

class SubInputExtractor(InputExtractor):
    def __init__(self, parent_extractor, *, channel_ids=None, start_frame=None, end_frame=None, epoch_name=None):
        self._parent_extractor=parent_extractor
        self._channel_ids=channel_ids
        if epoch_name is not None:
            e_info=parent_extractor.getEpochInfo(epoch_name)
            e_start=e_info['start_frame']
            e_end=e_info['end_frame']
            if start_frame is None:
                start_frame=e_start
            else:
                start_frame=e_start+start_frame
            if end_frame is None:
                end_frame=e_end
            else:
                end_frame=e_start+end_frame
        self._start_frame=start_frame
        self._end_frame=end_frame
        if self._channel_ids is None:
            self._channel_ids=range(self._parent_extractor.getNumChannels())
        if self._start_frame is None:
            self._start_frame=0
        if self._end_frame is None:
            self._end_frame=self._parent_extractor.getNumFrames()

    def getRawTraces(self, start_frame=None, end_frame=None, channel_ids=None):
        if start_frame is None:
            start_frame=0
        if end_frame is None:
            end_frame=self.getNumFrames()
        if channel_ids is None:
            channel_ids=range(self.getNumChannels())
        ch_ids=np.array(self._channel_ids)[channel_ids].tolist()
        sf=self._start_frame+start_frame
        ef=self._start_frame+end_frame
        return self._parent_extractor.getRawTraces(start_frame=sf,end_frame=ef,channel_ids=ch_ids)

    def getNumChannels(self):
        return len(self._channel_ids)

    def getNumFrames(self):
        return self._end_frame-self._start_frame

    def getSamplingFrequency(self):
        return self._parent_extractor.getSamplingFrequency()

    def frameToTime(self, frame):
        return self._parent_extractor.frameToTime(self._start_frame+frame)

    def timeToFrame(self, time):
        return self._parent_extractor.timeToFrame(time)-self._start_frame

    def getRawSnippets(self, snippet_len, center_frames, channel_ids=None):
        if channel_ids is None:
            channel_ids=range(self.getNumChannels())
        cf=self._start_frame+np.array(center_frames)
        ch_ids=np.array(self._channel_ids)[channel_ids].tolist()
        return self._parent_extractor.getRawSnippets(snippet_len=snippet_len,center_frames=cf,channel_ids=ch_ids)

    def getChannelInfo(self, channel_id):
        ch_id=self._channel_ids[channel_id]
        return self._parent_extractor.getChannelInfo(channel_id=ch_id)
