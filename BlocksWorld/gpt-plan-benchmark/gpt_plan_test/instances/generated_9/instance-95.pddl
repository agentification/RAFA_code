

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(ontable b)
(on c i)
(on d c)
(on e h)
(on f e)
(on g f)
(ontable h)
(on i a)
(clear d)
(clear g)
)
(:goal
(and
(on b f)
(on c e)
(on d i)
(on f h)
(on g b)
(on h c)
(on i a))
)
)


