#include "daisy_pod.h"
#include "daisysp.h"

#include "bufferplayer.h"

using namespace daisy;
using namespace daisysp;

struct BankHeader
{
    uint32_t numsamples;
    uint32_t datasize;
};

static const uint32_t MAX_BUFFER_SIZE = 44100 * 60 * 5;

static DaisyPod              hw;
static kn::BufferPlayer      bufferplayer;
static int16_t DSY_SDRAM_BSS buffer[MAX_BUFFER_SIZE];
static kn::SampleInfo        sampleinfo[kn::MAX_SAMPLES];
static BankHeader            bankheader;
Metro                        tick;

void AudioCallback(float **in, float **out, size_t size)
{
    hw.ProcessAllControls();
    for(size_t i = 0; i < size; i++)
    {
        bool t = tick.Process();

        if(t)
        {
            out[0][i] = out[1][i] = s162f(bufferplayer.Process());
        }
    }
}

void populatebuffer()
{
    SdmmcHandler::Config sd_cfg;
    SdmmcHandler         sdcard;
    size_t               bytesread;
    sd_cfg.width = SdmmcHandler::BusWidth::BITS_4;
    sd_cfg.speed = SdmmcHandler::Speed::VERY_FAST;
    sdcard.Init(sd_cfg);
    dsy_fatfs_init();
    hw.seed.PrintLine("Mounting drive.");
    f_mount(&SDFatFS, SDPath, 1);
    hw.seed.PrintLine("Opening file");
    f_open(&SDFile, "bank", FA_READ);
    f_read(&SDFile, &bankheader, sizeof(BankHeader), &bytesread);
    hw.seed.PrintLine("File read. %d samples found with size %d",
                      bankheader.numsamples,
                      bankheader.datasize);

    for(size_t i = 0; i < bankheader.numsamples; i++)
    {
        f_read(&SDFile, &sampleinfo[i], sizeof(kn::SampleInfo), &bytesread);
        hw.seed.PrintLine("Sample info %d loaded", i);
    }
    hw.seed.PrintLine("Reading bulk data");

    const uint16_t chunksize = 512;
    for(size_t i = 0; i < bankheader.datasize; i += chunksize)
    {
        f_read(&SDFile, &buffer[i], chunksize * sizeof(int16_t), &bytesread);
    }
    f_close(&SDFile);
    hw.seed.PrintLine("Closed file.");
}

int main(void)
{
    hw.Init();
    hw.StartAdc();
    float callbackrate = hw.AudioCallbackRate();
    float samplerate   = hw.AudioSampleRate();
    hw.seed.StartLog(true);
    populatebuffer();
    bufferplayer.Init(buffer, sampleinfo, bankheader.numsamples);
    tick.Init(41000, callbackrate);
    hw.StartAudio(AudioCallback);
    while(1)
    {
        bufferplayer.Trig(11);
        System::Delay(500);
        // bufferplayer.Trig(0);
        // bufferplayer.Trig(3);
        // System::Delay(500);
    }
}
