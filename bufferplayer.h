#pragma once
#include <stdint.h>
#include "math.h"

namespace kn
{
static const uint8_t MAX_POLYPHONY = 16;
static const uint8_t MAX_SAMPLES   = 16;

struct SampleInfo
{
    uint32_t offset;
    uint32_t frames;
};


class BufferPlayer
{
  private:
    int16_t*    buffer_;
    SampleInfo* sampleinfo_;
    uint8_t     numsamples_;
    bool        samplestatus_[MAX_SAMPLES];
    uint32_t    ptrposition[MAX_SAMPLES];

  public:
    void    Init(int16_t* buffer, SampleInfo* sampleinfo, uint8_t numsamples);
    int16_t Process();
    void    Trig(uint8_t sampleindex);
};

void kn::BufferPlayer::Init(int16_t*    buffer,
                            SampleInfo* sampleinfo,
                            uint8_t     numsamples)
{
    buffer_     = buffer;
    sampleinfo_ = sampleinfo;
    numsamples_ = numsamples;
}

void kn::BufferPlayer::Trig(uint8_t sampleindex)
{
    uint8_t index = std::min<uint8_t>(numsamples_ - 1, sampleindex);
    //NOTE: this might be better to do with an enum but we lose bool mult
    samplestatus_[index] = true;
}

int16_t kn::BufferPlayer::Process()
{
    int32_t output = 0;
    for(size_t i = 0; i < MAX_SAMPLES; i++)
    {
        // Check performance when using an if. This would allow us to use an enum
        output += buffer_[sampleinfo_[i].offset + ptrposition[i]]
                  * samplestatus_[i] * 0.3;
        ptrposition[i] += 1 * samplestatus_[i];

        if(ptrposition[i] >= sampleinfo_[i].frames)
        {
            ptrposition[i]   = 0;
            samplestatus_[i] = false;
        }
    }

    return static_cast<int16_t>(output);
}
} // namespace kn
