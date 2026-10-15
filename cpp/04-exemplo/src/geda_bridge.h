#ifndef GEDA_BRIDGE_H
#define GEDA_BRIDGE_H

#ifdef __cplusplus
extern "C" {
#endif

int geda_bridge_check(void);
int geda_bridge_list_components(const char *filename);
int geda_bridge_simulate(const char *filename);

#ifdef __cplusplus
}
#endif

#endif
