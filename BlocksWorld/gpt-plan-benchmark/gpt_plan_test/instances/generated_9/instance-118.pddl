

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b i)
(on c e)
(on d f)
(on e h)
(on f c)
(on g a)
(ontable h)
(ontable i)
(clear d)
(clear g)
)
(:goal
(and
(on b i)
(on c h)
(on d b)
(on e f)
(on f a)
(on h e)
(on i g))
)
)


