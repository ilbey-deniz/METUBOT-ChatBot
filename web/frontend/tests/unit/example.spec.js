import { shallowMount } from '@vue/test-utils'
import TheChat from '@/components/MetubotChat.vue'

describe('MetubotChat.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = shallowMount(TheChat, {
      propsData: { msg }
    })
    expect(wrapper.text()).toMatch(msg)
  })
})
